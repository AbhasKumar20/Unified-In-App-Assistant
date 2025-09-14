"""
Data Manager - Handles all data loading, persistence, and access control
"""
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import uuid

class DataManager:
    """Centralized data management with role-based access control"""
    
    def __init__(self, data_dir: str = "sample_data"):
        self.data_dir = data_dir
        self._cache = {}
        self._load_all_data()
    
    def _load_all_data(self):
        """Load all JSON data files into memory"""
        data_files = [
            'invoices_enhanced.json',
            'vendors_enhanced.json', 
            'users.json',
            'conversations_enhanced.json',
            'support_tickets.json',
            'reports.json',
            'allowed_actions.json'
        ]
        
        for file in data_files:
            file_path = os.path.join(self.data_dir, file)
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    data_key = file.replace('.json', '').replace('_enhanced', '')
                    self._cache[data_key] = json.load(f)
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        """Get user information by ID"""
        users = self._cache.get('users', {}).get('users', [])
        return next((user for user in users if user['id'] == user_id), None)
    
    def get_user_permissions(self, user_id: str) -> Dict:
        """Get user permissions"""
        user = self.get_user_by_id(user_id)
        return user.get('permissions', {}) if user else {}
    
    def get_user_role(self, user_id: str) -> str:
        """Get user role"""
        user = self.get_user_by_id(user_id)
        return user.get('role', 'report_viewer') if user else 'report_viewer'
    
    def get_allowed_actions(self, user_id: str) -> List[Dict]:
        """Get allowed actions for a user based on their role"""
        role = self.get_user_role(user_id)
        actions = self._cache.get('allowed_actions', {}).get('allowed_actions', {})
        return actions.get(role, [])
    
    def can_perform_action(self, user_id: str, action: str) -> bool:
        """Check if user can perform a specific action"""
        allowed_actions = self.get_allowed_actions(user_id)
        return any(a['action'] == action for a in allowed_actions)
    
    def filter_invoices(self, user_id: str, filters: Dict) -> List[Dict]:
        """Filter invoices based on criteria and user permissions"""
        if not self.can_perform_action(user_id, 'filter_invoices'):
            return []
        
        invoices = self._cache.get('invoices', {}).get('invoices', [])
        user = self.get_user_by_id(user_id)
        workspace_id = user.get('workspace_id') if user else None
        
        # Filter by workspace
        if workspace_id:
            invoices = [inv for inv in invoices if inv.get('workspace_id') == workspace_id]
        
        # Apply user filters
        filtered = invoices
        
        # Date range filter
        if 'date_range' in filters:
            start_date = filters['date_range'].get('start')
            end_date = filters['date_range'].get('end')
            if start_date and end_date:
                filtered = [
                    inv for inv in filtered 
                    if start_date <= inv.get('date', '') <= end_date
                ]
        
        # Vendor filter
        if 'vendor' in filters:
            filtered = [
                inv for inv in filtered 
                if inv.get('vendor', '').lower() == filters['vendor'].lower()
            ]
        
        # Status filter
        if 'status' in filters:
            filtered = [
                inv for inv in filtered 
                if inv.get('status', '').lower() == filters['status'].lower()
            ]
        
        # Amount range filter
        if 'amount_range' in filters:
            min_amount = filters['amount_range'].get('min', 0)
            max_amount = filters['amount_range'].get('max', float('inf'))
            filtered = [
                inv for inv in filtered 
                if min_amount <= inv.get('amount', 0) <= max_amount
            ]
        
        return filtered
    
    def get_invoice_by_id(self, invoice_id: str) -> Optional[Dict]:
        """Get invoice by ID"""
        invoices = self._cache.get('invoices', {}).get('invoices', [])
        return next((inv for inv in invoices if inv['id'] == invoice_id), None)
    
    def get_vendor_by_name(self, vendor_name: str) -> Optional[Dict]:
        """Get vendor by name"""
        vendors = self._cache.get('vendors', {}).get('vendors', [])
        return next((v for v in vendors if v['name'].lower() == vendor_name.lower()), None)
    
    def analyze_invoice_failures(self, user_id: str, invoice_ids: List[str]) -> Dict:
        """Analyze why invoices failed"""
        if not self.can_perform_action(user_id, 'analyze_failures'):
            return {}
        
        invoices = [self.get_invoice_by_id(inv_id) for inv_id in invoice_ids]
        invoices = [inv for inv in invoices if inv]  # Remove None values
        
        failure_analysis = {
            'total_invoices': len(invoices),
            'failure_reasons': {},
            'total_amount': 0,
            'affected_vendors': set(),
            'compliance_issues': []
        }
        
        for invoice in invoices:
            # Count failure reasons
            reason = invoice.get('failure_reason', 'unknown')
            failure_analysis['failure_reasons'][reason] = failure_analysis['failure_reasons'].get(reason, 0) + 1
            
            # Sum amounts
            failure_analysis['total_amount'] += invoice.get('amount', 0)
            
            # Track vendors
            failure_analysis['affected_vendors'].add(invoice.get('vendor', 'Unknown'))
            
            # Compliance issues
            if reason == 'missing_gstin':
                failure_analysis['compliance_issues'].append({
                    'invoice_id': invoice['id'],
                    'issue': 'GSTIN required for B2B transactions >₹500',
                    'vendor': invoice.get('vendor'),
                    'amount': invoice.get('amount')
                })
        
        failure_analysis['affected_vendors'] = list(failure_analysis['affected_vendors'])
        return failure_analysis
    
    def create_support_ticket(self, user_id: str, title: str, description: str, 
                            priority: str = 'medium', affected_invoices: List[str] = None) -> str:
        """Create a new support ticket"""
        if not self.can_perform_action(user_id, 'create_support_ticket'):
            return None
        
        ticket_id = f"TKT-{datetime.now().strftime('%Y')}-{str(uuid.uuid4())[:3].upper()}"
        
        ticket = {
            'id': ticket_id,
            'title': title,
            'description': description,
            'status': 'open',
            'priority': priority,
            'created_by': user_id,
            'assigned_to': 'compliance_team',
            'created_date': datetime.now().isoformat() + 'Z',
            'resolved_date': None,
            'workspace_id': self.get_user_by_id(user_id).get('workspace_id'),
            'affected_invoices': affected_invoices or [],
            'resolution': None,
            'updates': [{
                'timestamp': datetime.now().isoformat() + 'Z',
                'status': 'open',
                'note': 'Ticket created automatically by assistant',
                'updated_by': 'system'
            }],
            'conversation_id': None
        }
        
        # Add to cache
        if 'support_tickets' not in self._cache:
            self._cache['support_tickets'] = {'support_tickets': []}
        
        self._cache['support_tickets']['support_tickets'].append(ticket)
        
        # Save to file
        self._save_support_tickets()
        
        return ticket_id
    
    def get_support_tickets(self, user_id: str, status: str = None) -> List[Dict]:
        """Get support tickets for user"""
        tickets = self._cache.get('support_tickets', {}).get('support_tickets', [])
        user = self.get_user_by_id(user_id)
        workspace_id = user.get('workspace_id') if user else None
        
        # Filter by workspace
        if workspace_id:
            tickets = [t for t in tickets if t.get('workspace_id') == workspace_id]
        
        # Filter by status if specified
        if status:
            tickets = [t for t in tickets if t.get('status') == status]
        
        # Role-based filtering
        role = self.get_user_role(user_id)
        if role == 'report_viewer':
            # Can only see own tickets
            tickets = [t for t in tickets if t.get('created_by') == user_id]
        
        return tickets
    
    def get_conversations(self, user_id: str) -> List[Dict]:
        """Get conversation history for user"""
        conversations = self._cache.get('conversations', {}).get('conversations', [])
        return [conv for conv in conversations if conv.get('user_id') == user_id]
    
    def save_conversation_message(self, user_id: str, role: str, content: str, 
                                 actions_performed: List[Dict] = None, 
                                 data_shown: Dict = None, 
                                 explanation: Dict = None) -> str:
        """Save a new conversation message"""
        conversations = self._cache.get('conversations', {}).get('conversations', [])
        
        # Find or create conversation for today
        today = datetime.now().strftime('%Y-%m-%d')
        user_conversations = [c for c in conversations if c.get('user_id') == user_id]
        
        # Get the most recent conversation or create new one
        current_conv = None
        if user_conversations:
            # Check if the last conversation is from today
            last_conv = max(user_conversations, key=lambda x: x.get('last_updated', ''))
            last_date = last_conv.get('last_updated', '')[:10]  # Get date part
            if last_date == today:
                current_conv = last_conv
        
        if not current_conv:
            # Create new conversation
            conv_id = f"conv_{str(uuid.uuid4())[:8]}"
            current_conv = {
                'id': conv_id,
                'user_id': user_id,
                'workspace_id': self.get_user_by_id(user_id).get('workspace_id'),
                'started_date': datetime.now().isoformat() + 'Z',
                'last_updated': datetime.now().isoformat() + 'Z',
                'status': 'active',
                'messages': []
            }
            conversations.append(current_conv)
        
        # Add message
        message_id = f"msg_{str(uuid.uuid4())[:8]}"
        message = {
            'id': message_id,
            'timestamp': datetime.now().isoformat() + 'Z',
            'role': role,
            'content': content
        }
        
        if actions_performed:
            message['actions_performed'] = actions_performed
        
        if data_shown:
            message['data_shown'] = data_shown
        
        if explanation:
            message['explanation'] = explanation
        
        current_conv['messages'].append(message)
        current_conv['last_updated'] = datetime.now().isoformat() + 'Z'
        
        # Update cache
        self._cache['conversations'] = {'conversations': conversations}
        
        # Save to file
        self._save_conversations()
        
        return message_id
    
    def generate_report(self, user_id: str, report_type: str, parameters: Dict) -> Dict:
        """Generate a report based on type and parameters"""
        if not self.can_perform_action(user_id, 'generate_report'):
            return {}
        
        report_id = f"rpt_{str(uuid.uuid4())[:8]}"
        timestamp = datetime.now().isoformat() + 'Z'
        
        # Generate report based on type
        if report_type == 'compliance_status':
            return self._generate_compliance_report(user_id, report_id, timestamp, parameters)
        elif report_type == 'profit_loss':
            return self._generate_pl_report(user_id, report_id, timestamp, parameters)
        elif report_type == 'vendor_analysis':
            return self._generate_vendor_report(user_id, report_id, timestamp, parameters)
        
        return {}
    
    def _generate_compliance_report(self, user_id: str, report_id: str, timestamp: str, parameters: Dict) -> Dict:
        """Generate compliance status report"""
        vendor = parameters.get('vendor')
        date_range = parameters.get('date_range', {})
        
        # Filter invoices
        filters = {'vendor': vendor, 'date_range': date_range} if vendor else {'date_range': date_range}
        invoices = self.filter_invoices(user_id, filters)
        
        processed = [inv for inv in invoices if inv.get('status') == 'processed']
        failed = [inv for inv in invoices if inv.get('status') == 'failed']
        
        total_amount = sum(inv.get('amount', 0) for inv in invoices)
        processed_amount = sum(inv.get('amount', 0) for inv in processed)
        
        report = {
            'id': report_id,
            'name': f"{vendor}_Compliance_Report_{datetime.now().strftime('%b%Y')}.pdf" if vendor else f"Compliance_Report_{datetime.now().strftime('%b%Y')}.pdf",
            'type': 'compliance_status',
            'generated_date': timestamp,
            'generated_by': user_id,
            'workspace_id': self.get_user_by_id(user_id).get('workspace_id'),
            'parameters': parameters,
            'summary': {
                'total_invoices': len(invoices),
                'processed_invoices': len(processed),
                'failed_invoices': len(failed),
                'total_amount': total_amount,
                'processed_amount': processed_amount,
                'compliance_rate': (len(processed) / len(invoices) * 100) if invoices else 0
            },
            'file_path': f"/reports/{report_id}.pdf",
            'access_level': 'workspace',
            'data_sources': ['invoices', 'support_tickets', 'vendors']
        }
        
        return report
    
    def _save_support_tickets(self):
        """Save support tickets to file"""
        file_path = os.path.join(self.data_dir, 'support_tickets.json')
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self._cache['support_tickets'], f, indent=2, ensure_ascii=False)
    
    def _save_conversations(self):
        """Save conversations to file"""
        file_path = os.path.join(self.data_dir, 'conversations_enhanced.json')
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self._cache['conversations'], f, indent=2, ensure_ascii=False)
    
    def get_all_users(self) -> List[Dict]:
        """Get all users for role switching demo"""
        return self._cache.get('users', {}).get('users', [])
    
    def parse_natural_language_date(self, date_text: str) -> Dict:
        """Parse natural language date expressions"""
        # For demo purposes, use 2024 data when "last month" is mentioned
        if 'last month' in date_text.lower():
            # Return August 2024 for our sample data
            return {
                'start': '2024-08-01',
                'end': '2024-08-31'
            }
        elif 'this month' in date_text.lower():
            # Return September 2024 for demo consistency
            return {
                'start': '2024-09-01',
                'end': '2024-09-30'
            }
        
        return {}
