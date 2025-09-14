"""
Action Processor - Handles natural language processing and action execution
"""
import re
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import uuid

class ActionProcessor:
    """Processes natural language inputs and executes corresponding actions"""
    
    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.action_patterns = self._initialize_action_patterns()
    
    def _initialize_action_patterns(self) -> Dict[str, Dict]:
        """Initialize regex patterns for different action types"""
        return {
            'filter_invoices': {
                'patterns': [
                    r'filter\s+invoices?\s+for\s+(.+?)(?:,|$)',
                    r'show\s+invoices?\s+(?:for\s+)?(.+?)(?:,|$)',
                    r'find\s+invoices?\s+(?:for\s+)?(.+?)(?:,|$)',
                    r'get\s+invoices?\s+(?:for\s+)?(.+?)(?:,|$)'
                ],
                'parameter_patterns': {
                    'date_range': [
                        r'last\s+month',
                        r'this\s+month', 
                        r'(\d{4}-\d{2}-\d{2})\s+to\s+(\d{4}-\d{2}-\d{2})',
                        r'from\s+(\d{4}-\d{2}-\d{2})\s+to\s+(\d{4}-\d{2}-\d{2})'
                    ],
                    'vendor': [
                        r"vendor\s*=\s*['\"]([^'\"]+)['\"]",
                        r"vendor\s*=\s*([A-Za-z][A-Za-z0-9\s]*[A-Za-z0-9])",
                        r"vendor\s*[=:]\s*([A-Za-z][A-Za-z0-9\s]*[A-Za-z0-9])",
                        r"from\s+([A-Za-z][A-Za-z\s]*[A-Za-z])"
                    ],
                    'status': [
                        r"status\s*=\s*['\"]([^'\"]+)['\"]",
                        r"status\s*=\s*([^,\s\.]+)",
                        r"status\s*[=:]\s*([^,\s\.]+)",
                        r"pending\s+approval",
                        r"(failed|processed|pending|completed)"
                    ],
                    'amount': [
                        r"amount\s*>\s*(\d+)",
                        r"amount\s*<\s*(\d+)",
                        r"amount\s*=\s*(\d+)"
                    ]
                }
            },
            'explain_failures': {
                'patterns': [
                    r'why\s+did\s+(?:this|these|they)\s+fail\??',
                    r'what\s+(?:caused|made)\s+(?:this|these|them)\s+(?:to\s+)?fail\??',
                    r'explain\s+(?:the\s+)?failures?',
                    r'what\s+went\s+wrong\??'
                ]
            },
            'create_ticket': {
                'patterns': [
                    r'create\s+(?:a\s+)?ticket',
                    r'open\s+(?:a\s+)?ticket',
                    r'file\s+(?:a\s+)?ticket',
                    r'report\s+(?:this\s+)?(?:issue|problem)'
                ],
                'parameter_patterns': {
                    'notify': [r'notify\s+me\s+when\s+(fixed|resolved|done)']
                }
            },
            'download_report': {
                'patterns': [
                    r'download\s+(?:the\s+)?(.+?)\s+report',
                    r'generate\s+(?:and\s+)?download\s+(.+?)\s+report',
                    r'get\s+(?:the\s+)?(.+?)\s+report',
                    r'export\s+(?:the\s+)?(.+?)\s+report'
                ]
            },
            'general_question': {
                'patterns': [
                    r'what\s+is\s+(.+?)\??',
                    r'how\s+(?:does|do)\s+(.+?)\s+work\??',
                    r'tell\s+me\s+about\s+(.+?)\??'
                ]
            }
        }
    
    def process_input(self, user_input: str, user_id: str, context: Dict = None) -> Dict:
        """Process natural language input and return action result"""
        user_input = user_input.strip()
        
        # Detect action type
        action_type = self._detect_action_type(user_input)
        
        if action_type == 'filter_invoices':
            return self._handle_filter_invoices(user_input, user_id)
        elif action_type == 'explain_failures':
            return self._handle_explain_failures(user_input, user_id, context)
        elif action_type == 'create_ticket':
            return self._handle_create_ticket(user_input, user_id, context)
        elif action_type == 'download_report':
            return self._handle_download_report(user_input, user_id, context)
        elif action_type == 'general_question':
            return self._handle_general_question(user_input, user_id, context)
        else:
            return self._handle_unknown_input(user_input, user_id)
    
    def _detect_action_type(self, user_input: str) -> str:
        """Detect the type of action from user input"""
        user_input_lower = user_input.lower()
        
        # Handle affirmative responses that should trigger ticket creation
        if user_input_lower.strip() in ['yes', 'y', 'sure', 'ok', 'okay', 'please', 'create it', 'do it']:
            return 'create_ticket'
        
        for action_type, config in self.action_patterns.items():
            for pattern in config['patterns']:
                if re.search(pattern, user_input_lower):
                    return action_type
        
        return 'general_question'
    
    def _extract_parameters(self, user_input: str, action_type: str) -> Dict:
        """Extract parameters from user input based on action type"""
        parameters = {}
        
        if action_type not in self.action_patterns:
            return parameters
        
        param_patterns = self.action_patterns[action_type].get('parameter_patterns', {})
        
        for param_name, patterns in param_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, user_input, re.IGNORECASE)
                if match:
                    if param_name == 'date_range':
                        if 'last month' in match.group(0).lower():
                            parameters['date_range'] = self.data_manager.parse_natural_language_date('last month')
                        elif 'this month' in match.group(0).lower():
                            parameters['date_range'] = self.data_manager.parse_natural_language_date('this month')
                        elif match.groups() and len(match.groups()) >= 2:
                            parameters['date_range'] = {
                                'start': match.group(1),
                                'end': match.group(2)
                            }
                    else:
                        # Handle special cases for status
                        if param_name == 'status' and 'pending approval' in match.group(0).lower():
                            parameters[param_name] = 'pending_approval'
                        else:
                            # Clean up the extracted parameter value
                            value = match.group(1).strip()
                            # Remove trailing punctuation
                            value = value.rstrip('.,!?')
                            # Remove quotes if present (handle nested quotes)
                            if value.startswith("'") and value.endswith("'"):
                                value = value[1:-1]
                            elif value.startswith('"') and value.endswith('"'):
                                value = value[1:-1]
                            # Handle case where quotes are part of the extracted text
                            if value.startswith("'") or value.startswith('"'):
                                value = value[1:]
                            if value.endswith("'") or value.endswith('"'):
                                value = value[:-1]
                            parameters[param_name] = value
                    break
        
        return parameters
    
    def _handle_filter_invoices(self, user_input: str, user_id: str) -> Dict:
        """Handle invoice filtering requests"""
        parameters = self._extract_parameters(user_input, 'filter_invoices')
        
        # Execute the filter
        invoices = self.data_manager.filter_invoices(user_id, parameters)
        
        # Calculate summary stats
        total_amount = sum(inv.get('amount', 0) for inv in invoices)
        failure_reasons = {}
        for inv in invoices:
            reason = inv.get('failure_reason', 'N/A')
            failure_reasons[reason] = failure_reasons.get(reason, 0) + 1
        
        # Create response
        response_parts = []
        if invoices:
            response_parts.append(f"I found {len(invoices)} invoices")
            
            # Add filter details
            if parameters.get('vendor'):
                response_parts.append(f"from {parameters['vendor']}")
            if parameters.get('date_range'):
                date_range = parameters['date_range']
                response_parts.append(f"for {date_range['start']} to {date_range['end']}")
            if parameters.get('status'):
                response_parts.append(f"with status '{parameters['status']}'")
            
            response_parts.append(f". Total amount: ₹{total_amount:,.2f}")
            
            # Add failure summary if applicable
            if parameters.get('status') == 'failed' and failure_reasons:
                if len(failure_reasons) == 1:
                    # Single failure reason
                    reason = list(failure_reasons.keys())[0]
                    if reason != 'N/A':
                        response_parts.append(f". All failures are due to {reason.replace('_', ' ')}")
                else:
                    # Multiple failure reasons
                    total_failed = sum(failure_reasons.values())
                    reason_list = []
                    for reason, count in failure_reasons.items():
                        if reason != 'N/A':
                            reason_list.append(f"{reason.replace('_', ' ')} ({count})")
                    if reason_list:
                        response_parts.append(f". Failure reasons: {', '.join(reason_list)}")
        else:
            response_parts.append("No invoices found matching your criteria")
        
        content = " ".join(response_parts) + "."
        
        # Record action performed
        actions_performed = [{
            'action': 'filter_invoices',
            'parameters': parameters,
            'results_count': len(invoices),
            'data_consulted': ['invoices', 'vendors']
        }]
        
        # Data to show in UI
        data_shown = {
            'invoice_ids': [inv['id'] for inv in invoices],
            'total_amount': total_amount,
            'invoices': invoices[:10]  # Show first 10 for display
        }
        
        # Add failure_reasons only if there are failed invoices
        if failure_reasons and any(reason != 'N/A' for reason in failure_reasons.keys()):
            data_shown['failure_reasons'] = failure_reasons
        
        return {
            'content': content,
            'actions_performed': actions_performed,
            'data_shown': data_shown,
            'context_update': {
                'last_filtered_invoices': [inv['id'] for inv in invoices],
                'last_filter_parameters': parameters
            }
        }
    
    def _handle_explain_failures(self, user_input: str, user_id: str, context: Dict = None) -> Dict:
        """Handle failure explanation requests"""
        # Get invoice IDs from context
        invoice_ids = []
        if context and 'last_filtered_invoices' in context:
            invoice_ids = context['last_filtered_invoices']
        
        if not invoice_ids:
            return {
                'content': "I don't have any recent invoice data to analyze. Please filter some invoices first.",
                'actions_performed': [],
                'data_shown': {}
            }
        
        # Analyze failures
        analysis = self.data_manager.analyze_invoice_failures(user_id, invoice_ids)
        
        # Generate explanation
        content_parts = []
        
        if analysis.get('failure_reasons'):
            total_invoices = analysis.get('total_invoices', 0)
            failure_reasons = analysis.get('failure_reasons', {})
            
            if len(failure_reasons) == 1:
                # Single failure reason
                reason_name, count = list(failure_reasons.items())[0]
                
                if reason_name == 'missing_gstin':
                    content_parts.append(f"All {count} invoice{'s' if count != 1 else ''} failed because GSTIN (GST Identification Number) is missing from the invoice files.")
                    content_parts.append("Indian tax law requires GSTIN for B2B transactions above ₹500.")
                elif reason_name == 'invalid_amount':
                    content_parts.append(f"All {count} invoice{'s' if count != 1 else ''} failed due to invalid amount calculations.")
                    content_parts.append("The invoice amounts don't match the purchase order or have calculation errors.")
                elif reason_name == 'duplicate_invoice':
                    content_parts.append(f"All {count} invoice{'s' if count != 1 else ''} failed because they are duplicates.")
                    content_parts.append("These invoices have already been submitted and processed previously.")
                elif reason_name == 'expired_po':
                    content_parts.append(f"All {count} invoice{'s' if count != 1 else ''} failed because the purchase order has expired.")
                    content_parts.append("The invoices reference purchase orders that are no longer valid.")
                elif reason_name == 'missing_documentation':
                    content_parts.append(f"All {count} invoice{'s' if count != 1 else ''} failed due to missing supporting documentation.")
                    content_parts.append("Required supporting documents like delivery receipts or contracts are not attached.")
                else:
                    content_parts.append(f"All {count} invoice{'s' if count != 1 else ''} failed due to {reason_name.replace('_', ' ')}.")
                
                # List specific invoices for single failure type
                invoices_list = []
                for invoice_id in invoice_ids[:7]:  # Show first 7
                    invoice = self.data_manager.get_invoice_by_id(invoice_id)
                    if invoice and invoice.get('failure_reason') == reason_name:
                        invoices_list.append(invoice.get('invoice_number', invoice_id))
                
                if invoices_list:
                    content_parts.append(f"The invoice{'s' if len(invoices_list) != 1 else ''}: {', '.join(invoices_list)}.")
            
            else:
                # Multiple failure reasons
                content_parts.append(f"The {total_invoices} invoices failed for different reasons:")
                
                for reason_name, count in failure_reasons.items():
                    if reason_name == 'missing_gstin':
                        content_parts.append(f"• {count} invoice{'s' if count != 1 else ''}: Missing GSTIN")
                    elif reason_name == 'invalid_amount':
                        content_parts.append(f"• {count} invoice{'s' if count != 1 else ''}: Invalid amount calculation")
                    elif reason_name == 'duplicate_invoice':
                        content_parts.append(f"• {count} invoice{'s' if count != 1 else ''}: Duplicate submission")
                    elif reason_name == 'expired_po':
                        content_parts.append(f"• {count} invoice{'s' if count != 1 else ''}: Expired purchase order")
                    elif reason_name == 'missing_documentation':
                        content_parts.append(f"• {count} invoice{'s' if count != 1 else ''}: Missing documentation")
                    else:
                        content_parts.append(f"• {count} invoice{'s' if count != 1 else ''}: {reason_name.replace('_', ' ')}")
        
        # Add proactive ticket creation offer for compliance issues
        if 'missing_gstin' in analysis.get('failure_reasons', {}) or 'missing_documentation' in analysis.get('failure_reasons', {}):
            content_parts.append("\n\nWould you like me to create a ticket and notify you when this is fixed?")
        
        content = " ".join(content_parts)
        
        # Record action
        actions_performed = [{
            'action': 'analyze_failures',
            'parameters': {'invoice_ids': invoice_ids},
            'data_consulted': ['invoices', 'compliance_rules', 'vendors']
        }]
        
        # Explanation details
        explanation = {
            'root_cause': list(analysis.get('failure_reasons', {}).keys())[0] if analysis.get('failure_reasons') else 'unknown',
            'affected_files': analysis.get('total_invoices', 0),
            'compliance_requirement': 'GSTIN mandatory for B2B transactions >₹500' if 'missing_gstin' in analysis.get('failure_reasons', {}) else 'Various compliance requirements',
            'next_steps': 'Contact vendor for updated invoices with GSTIN' if 'missing_gstin' in analysis.get('failure_reasons', {}) else 'Review specific failure reasons',
            'suggested_action': 'Create support ticket for GSTIN compliance issue' if 'missing_gstin' in analysis.get('failure_reasons', {}) else None
        }
        
        return {
            'content': content,
            'actions_performed': actions_performed,
            'data_shown': analysis,
            'explanation': explanation,
            'context_update': {
                'last_analysis': analysis,
                'analyzed_invoices': invoice_ids
            }
        }
    
    def _handle_create_ticket(self, user_input: str, user_id: str, context: Dict = None) -> Dict:
        """Handle support ticket creation"""
        # Extract parameters
        parameters = self._extract_parameters(user_input, 'create_ticket')
        
        # Get context for ticket details
        invoice_ids = []
        if context and 'last_filtered_invoices' in context:
            invoice_ids = context['last_filtered_invoices']
        
        # Determine ticket details based on context
        title = "General Support Request"
        description = "Support request created via assistant"
        priority = 'medium'
        
        if context and 'last_analysis' in context:
            analysis = context['last_analysis']
            if 'missing_gstin' in analysis.get('failure_reasons', {}):
                title = "Missing GSTIN in vendor invoices"
                vendor_names = list(analysis.get('affected_vendors', []))
                vendor_text = vendor_names[0] if vendor_names else "vendor"
                count = analysis.get('total_invoices', 0)
                amount = analysis.get('total_amount', 0)
                
                description = f"{count} invoices from {vendor_text} failed processing due to missing GSTIN. "
                description += f"Total amount affected: ₹{amount:,.2f}. "
                description += "Requires vendor to provide GSTIN and resubmit invoices."
                priority = 'high'
        
        # Create the ticket
        ticket_id = self.data_manager.create_support_ticket(
            user_id=user_id,
            title=title,
            description=description,
            priority=priority,
            affected_invoices=invoice_ids
        )
        
        # Generate response
        content = f"Created support ticket #{ticket_id}: '{title}'. "
        
        if 'notify' in parameters:
            content += "I'll notify you when the vendor provides updated invoices. "
        
        content += "Ticket assigned to compliance team."
        
        # Record action
        actions_performed = [{
            'action': 'create_support_ticket',
            'parameters': {
                'title': title,
                'priority': priority,
                'affected_invoices': invoice_ids
            },
            'ticket_id': ticket_id
        }]
        
        return {
            'content': content,
            'actions_performed': actions_performed,
            'data_shown': {},
            'ticket_created': {
                'id': ticket_id,
                'status': 'open',
                'assigned_to': 'compliance_team'
            },
            'context_update': {
                'last_ticket_created': ticket_id
            }
        }
    
    def _handle_download_report(self, user_input: str, user_id: str, context: Dict = None) -> Dict:
        """Handle report download requests"""
        # Extract report type from input
        match = re.search(r'download\s+(?:the\s+)?(.+?)\s+report', user_input, re.IGNORECASE)
        report_type_text = match.group(1) if match else 'compliance'
        
        # Determine report type and parameters
        if 'fixed' in report_type_text.lower() or 'compliance' in report_type_text.lower():
            report_type = 'compliance_status'
            
            # Get vendor from context or input
            vendor = None
            if context and 'last_filter_parameters' in context:
                vendor = context['last_filter_parameters'].get('vendor')
            
            # Set date range to current month
            parameters = {
                'report_type': report_type,
                'date_range': {
                    'start': datetime.now().strftime('%Y-%m-01'),
                    'end': datetime.now().strftime('%Y-%m-%d')
                }
            }
            
            if vendor:
                parameters['vendor'] = vendor
        else:
            report_type = 'general'
            parameters = {'report_type': 'general'}
        
        # Generate the report
        report = self.data_manager.generate_report(user_id, report_type, parameters)
        
        if not report:
            return {
                'content': "Sorry, I couldn't generate the report. Please check your permissions.",
                'actions_performed': [],
                'data_shown': {}
            }
        
        # Generate response
        report_name = report.get('name', 'report.pdf')
        summary = report.get('summary', {})
        
        content_parts = [f"Generated and downloaded '{report_name}'."]
        
        if report_type == 'compliance_status':
            processed_count = summary.get('processed_invoices', 0)
            processed_amount = summary.get('processed_amount', 0)
            failed_count = summary.get('failed_invoices', 0)
            
            content_parts.append(f"Report shows {processed_count} invoice{'s' if processed_count != 1 else ''} processed (₹{processed_amount:,.0f})")
            
            if failed_count > 0:
                content_parts.append(f" with valid GSTIN. {failed_count} remaining invoice{'s' if failed_count != 1 else ''} still need vendor correction.")
            else:
                content_parts.append(" with valid GSTIN.")
        
        content = " ".join(content_parts)
        
        # Record action
        actions_performed = [{
            'action': 'generate_report',
            'parameters': parameters,
            'file_generated': report_name,
            'data_consulted': report.get('data_sources', [])
        }]
        
        return {
            'content': content,
            'actions_performed': actions_performed,
            'data_shown': {},
            'report_summary': summary,
            'context_update': {
                'last_report_generated': report.get('id')
            }
        }
    
    def _handle_general_question(self, user_input: str, user_id: str, context: Dict = None) -> Dict:
        """Handle general questions and provide helpful responses"""
        content = "I can help you with:\n"
        content += "• Filtering invoices: 'Filter invoices for last month, vendor=IndiSky, status=failed'\n"
        content += "• Explaining issues: 'Why did these fail?'\n" 
        content += "• Creating tickets: 'Create a ticket and notify me when fixed'\n"
        content += "• Downloading reports: 'Download the compliance report'\n"
        content += "\nWhat would you like to do?"
        
        return {
            'content': content,
            'actions_performed': [],
            'data_shown': {}
        }
    
    def _handle_unknown_input(self, user_input: str, user_id: str) -> Dict:
        """Handle inputs that don't match any known patterns"""
        return {
            'content': "I'm not sure how to help with that. Try asking me to filter invoices, explain failures, create tickets, or download reports.",
            'actions_performed': [],
            'data_shown': {}
        }
