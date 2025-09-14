"""
Context Manager - Handles conversation context, continuity, and session management
"""
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta

class ContextManager:
    """Manages conversation context and cross-session continuity"""
    
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.session_context = {}
    
    def get_user_context(self, user_id: str) -> Dict:
        """Get comprehensive context for a user including conversation history and updates"""
        context = {
            'user_info': self.data_manager.get_user_by_id(user_id),
            'recent_conversations': self._get_recent_conversations(user_id),
            'open_tickets': self._get_open_tickets(user_id),
            'recent_updates': self._get_recent_updates(user_id),
            'session_data': self.session_context.get(user_id, {}),
            'context_summary': self._generate_context_summary(user_id)
        }
        
        return context
    
    def update_session_context(self, user_id: str, updates: Dict):
        """Update session context with new information"""
        if user_id not in self.session_context:
            self.session_context[user_id] = {}
        
        self.session_context[user_id].update(updates)
    
    def get_session_context(self, user_id: str) -> Dict:
        """Get current session context"""
        return self.session_context.get(user_id, {})
    
    def clear_session_context(self, user_id: str):
        """Clear session context for user"""
        if user_id in self.session_context:
            del self.session_context[user_id]
    
    def _get_recent_conversations(self, user_id: str) -> List[Dict]:
        """Get recent conversation history"""
        conversations = self.data_manager.get_conversations(user_id)
        
        # Sort by last updated and get recent ones
        recent_conversations = sorted(
            conversations, 
            key=lambda x: x.get('last_updated', ''), 
            reverse=True
        )[:5]  # Last 5 conversations
        
        return recent_conversations
    
    def _get_open_tickets(self, user_id: str) -> List[Dict]:
        """Get open support tickets for user"""
        return self.data_manager.get_support_tickets(user_id, status='open')
    
    def _get_recent_updates(self, user_id: str) -> List[Dict]:
        """Get recent updates (resolved tickets, new invoices, etc.)"""
        updates = []
        
        # Check for recently resolved tickets
        all_tickets = self.data_manager.get_support_tickets(user_id)
        recent_resolved = [
            t for t in all_tickets 
            if t.get('status') == 'resolved' and self._is_recent(t.get('resolved_date'))
        ]
        
        for ticket in recent_resolved:
            updates.append({
                'type': 'ticket_resolved',
                'ticket_id': ticket['id'],
                'title': ticket['title'],
                'resolved_date': ticket['resolved_date'],
                'message': f"Ticket #{ticket['id']} has been resolved"
            })
        
        # Check for new invoices related to resolved issues
        # This would check if any new invoices were processed after ticket resolution
        for ticket in recent_resolved:
            if 'missing_gstin' in ticket.get('title', '').lower():
                # Look for new processed invoices from the same vendor
                affected_invoices = ticket.get('affected_invoices', [])
                if affected_invoices:
                    # Get vendor from first affected invoice
                    first_invoice = self.data_manager.get_invoice_by_id(affected_invoices[0])
                    if first_invoice:
                        vendor = first_invoice.get('vendor')
                        # Look for recent processed invoices from this vendor
                        recent_processed = self.data_manager.filter_invoices(user_id, {
                            'vendor': vendor,
                            'status': 'processed',
                            'date_range': self._get_recent_date_range()
                        })
                        
                        if recent_processed:
                            updates.append({
                                'type': 'new_processed_invoice',
                                'vendor': vendor,
                                'count': len(recent_processed),
                                'message': f"{vendor} provided corrected invoice{'s' if len(recent_processed) > 1 else ''}"
                            })
        
        return updates
    
    def _generate_context_summary(self, user_id: str) -> str:
        """Generate a summary of current context for display"""
        summary_parts = []
        
        # Open tickets summary
        open_tickets = self._get_open_tickets(user_id)
        if open_tickets:
            summary_parts.append(f"{len(open_tickets)} open ticket{'s' if len(open_tickets) > 1 else ''}")
        
        # Recent updates summary
        recent_updates = self._get_recent_updates(user_id)
        resolved_tickets = [u for u in recent_updates if u['type'] == 'ticket_resolved']
        if resolved_tickets:
            summary_parts.append(f"{len(resolved_tickets)} recently resolved ticket{'s' if len(resolved_tickets) > 1 else ''}")
        
        # Session context summary
        session_data = self.get_session_context(user_id)
        if 'last_filtered_invoices' in session_data:
            count = len(session_data['last_filtered_invoices'])
            summary_parts.append(f"{count} invoice{'s' if count > 1 else ''} in recent filter")
        
        if summary_parts:
            return "Context: " + ", ".join(summary_parts)
        else:
            return "No active context"
    
    def generate_welcome_message(self, user_id: str) -> Dict:
        """Generate a welcome message with context updates"""
        user = self.data_manager.get_user_by_id(user_id)
        user_name = user.get('name', '').split()[0] if user else 'User'  # First name
        
        # For demo purposes, simulate the "next day" scenario
        recent_ticket = self._get_most_recent_ticket(user_id)
        if self._simulate_recent_resolution() and recent_ticket:
            message_parts = [f"Welcome back, {user_name}! 🔔 Context update:"]
            
            # Show the most recent ticket resolution update
            message_parts.append(f"Ticket #{recent_ticket['id']} has been resolved.")
            message_parts.append("IndiSky provided their GSTIN (27AABCI9999B1ZS) and sent corrected invoices.")
            
            # Check for any other open tickets
            open_tickets = self._get_open_tickets(user_id)
            if open_tickets:
                message_parts.append(f"You have {len(open_tickets)} other open tickets.")
            
            content = " ".join(message_parts)
            
            context_update = {
                'open_tickets': [t['id'] for t in open_tickets],
                'resolved_tickets': [recent_ticket['id']],
                'new_invoices': ['inv_009'],  # The corrected invoice
                'previous_context': f"IndiSky missing GSTIN issue - {recent_ticket['title']}"
            }
            
            return {
                'content': content,
                'context_update': context_update,
                'show_updates': True
            }
        else:
            # Check for updates since last session
            recent_updates = self._get_recent_updates(user_id)
            open_tickets = self._get_open_tickets(user_id)
            
            if recent_updates or open_tickets:
                # There are updates to show
                message_parts = [f"Welcome back, {user_name}! 🔔 Context update:"]
                
                # Show resolved tickets
                resolved_updates = [u for u in recent_updates if u['type'] == 'ticket_resolved']
                for update in resolved_updates:
                    message_parts.append(f"Ticket #{update['ticket_id']} has been resolved.")
                    
                    # Look for related new invoices
                    new_invoice_updates = [
                        u for u in recent_updates 
                        if u['type'] == 'new_processed_invoice'
                    ]
                    for inv_update in new_invoice_updates:
                        vendor = inv_update['vendor']
                        # Get vendor GSTIN for display
                        vendor_info = self.data_manager.get_vendor_by_name(vendor)
                        gstin = vendor_info.get('gstin') if vendor_info else 'Unknown'
                        message_parts.append(f"{vendor} provided their GSTIN ({gstin}) and sent a corrected invoice.")
                
                # Show remaining open tickets
                if open_tickets:
                    message_parts.append(f"\nOpen tickets: {len(open_tickets)}")
                
                content = " ".join(message_parts)
                
                context_update = {
                    'open_tickets': [t['id'] for t in open_tickets],
                    'resolved_tickets': [u['ticket_id'] for u in resolved_updates],
                    'new_invoices': [],  # Would be populated with actual new invoice IDs
                    'previous_context': self._get_previous_context_summary(user_id)
                }
                
                return {
                    'content': content,
                    'context_update': context_update,
                    'show_updates': True
                }
            else:
                # No updates, regular welcome
                return {
                    'content': f"Hello, {user_name}! How can I help you today?",
                    'context_update': {},
                    'show_updates': False
                }
    
    def _get_previous_context_summary(self, user_id: str) -> str:
        """Get a summary of previous context for reference"""
        recent_conversations = self._get_recent_conversations(user_id)
        
        if not recent_conversations:
            return ""
        
        # Get the most recent conversation
        last_conv = recent_conversations[0]
        last_messages = last_conv.get('messages', [])
        
        # Find the last user action
        user_messages = [m for m in last_messages if m.get('role') == 'user']
        if user_messages:
            last_user_message = user_messages[-1].get('content', '')
            if 'indisky' in last_user_message.lower() and 'gstin' in str(last_conv).lower():
                return "IndiSky missing GSTIN issue from previous session"
        
        return "Previous conversation context"
    
    def _is_recent(self, date_string: str, days: int = 7) -> bool:
        """Check if a date is within the last N days"""
        if not date_string:
            return False
        
        try:
            date_obj = datetime.fromisoformat(date_string.replace('Z', '+00:00'))
            return (datetime.now() - date_obj.replace(tzinfo=None)).days <= days
        except:
            return False
    
    def _get_most_recent_ticket(self, user_id: str) -> Dict:
        """Get the most recently created ticket for the user"""
        tickets = self.data_manager.get_support_tickets(user_id)
        if not tickets:
            return None
        
        # Sort by created_date and get the most recent
        tickets_sorted = sorted(tickets, key=lambda x: x.get('created_date', ''), reverse=True)
        return tickets_sorted[0] if tickets_sorted else None
    
    def _simulate_recent_resolution(self) -> bool:
        """For demo purposes, simulate that IndiSky GSTIN issue was recently resolved"""
        # In a real system, this would check actual recent updates
        # For demo, we'll show the resolution update
        return True
    
    def _get_recent_date_range(self, days: int = 7) -> Dict:
        """Get date range for recent items"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        return {
            'start': start_date.strftime('%Y-%m-%d'),
            'end': end_date.strftime('%Y-%m-%d')
        }
    
    def get_conversation_history_for_display(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Get formatted conversation history for UI display"""
        conversations = self._get_recent_conversations(user_id)
        
        history = []
        for conv in conversations:
            messages = conv.get('messages', [])
            
            # Add conversation header
            start_date = conv.get('started_date', '')
            if start_date:
                try:
                    date_obj = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                    date_str = date_obj.strftime('%B %d, %Y')
                    history.append({
                        'type': 'date_header',
                        'content': date_str,
                        'timestamp': start_date
                    })
                except:
                    pass
            
            # Add messages
            for msg in messages[-limit:]:  # Last N messages from each conversation
                history.append({
                    'type': 'message',
                    'role': msg.get('role'),
                    'content': msg.get('content'),
                    'timestamp': msg.get('timestamp'),
                    'actions_performed': msg.get('actions_performed', []),
                    'data_shown': msg.get('data_shown', {})
                })
        
        return history[:limit]
    
    def get_active_tickets_for_display(self, user_id: str) -> List[Dict]:
        """Get active support tickets formatted for display"""
        tickets = self.data_manager.get_support_tickets(user_id)
        
        # Format for display
        display_tickets = []
        for ticket in tickets:
            display_tickets.append({
                'id': ticket['id'],
                'title': ticket['title'],
                'status': ticket['status'],
                'priority': ticket['priority'],
                'created_date': ticket['created_date'],
                'resolved_date': ticket.get('resolved_date'),
                'summary': self._get_ticket_summary(ticket)
            })
        
        return display_tickets
    
    def _get_ticket_summary(self, ticket: Dict) -> str:
        """Generate a summary for a ticket"""
        status = ticket.get('status', 'unknown')
        title = ticket.get('title', 'No title')
        
        if status == 'resolved':
            return f"✅ {title} - Resolved"
        elif status == 'in_progress':
            return f"🔄 {title} - In Progress"
        elif status == 'open':
            return f"🔓 {title} - Open"
        else:
            return f"❓ {title} - {status.title()}"
