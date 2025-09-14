"""
FinKraft - Unified In-App Assistant
Main Streamlit Application
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import time
import uuid
from typing import Dict, List, Any

# Import our core modules
from core.data_manager import DataManager
from core.action_processor import ActionProcessor
from core.context_manager import ContextManager

# Page configuration
st.set_page_config(
    page_title="FinKraft Assistant",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS for modern, professional UI
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styling */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Main Header */
    .main-header {
        font-size: 2.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .subtitle {
        text-align: center;
        color: #64748b;
        font-size: 1.1rem;
        font-weight: 400;
        margin-bottom: 2rem;
    }
    
    /* Chat Messages */
    .chat-message {
        padding: 1.25rem;
        border-radius: 1rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border: 1px solid #e2e8f0;
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        margin-left: 2rem;
    }
    
    .assistant-message {
        background: #ffffff;
        border-left: 4px solid #10b981;
        margin-right: 2rem;
    }
    
    .context-update {
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
        color: white;
        border: none;
        font-weight: 500;
    }
    
    /* Cards and Components */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
        text-align: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.12);
    }
    
    .ticket-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 1rem;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        transition: all 0.2s ease;
    }
    
    .ticket-card:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        border-color: #c7d2fe;
    }
    
    /* Trace Items */
    .trace-item {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 0.75rem;
        padding: 1rem;
        margin: 0.5rem 0;
        font-family: 'SF Mono', 'Monaco', 'Cascadia Code', 'Roboto Mono', monospace;
        font-size: 0.9rem;
        color: #475569;
    }
    
    /* Sidebar Enhancements */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
    }
    
    /* Button Styling */
    .stButton > button {
        border-radius: 0.75rem;
        border: none;
        font-weight: 500;
        transition: all 0.2s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    /* Data Tables */
    .stDataFrame {
        border-radius: 1rem;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    /* Expander Styling */
    .streamlit-expanderHeader {
        background: #f8fafc;
        border-radius: 0.5rem;
        font-weight: 500;
    }
    
    /* Status Badges */
    .status-resolved { color: #10b981; font-weight: 600; }
    .status-open { color: #f59e0b; font-weight: 600; }
    .status-in-progress { color: #3b82f6; font-weight: 600; }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.3s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'data_manager' not in st.session_state:
    st.session_state.data_manager = DataManager()
    st.session_state.action_processor = ActionProcessor(st.session_state.data_manager)
    st.session_state.context_manager = ContextManager(st.session_state.data_manager)

if 'current_user_id' not in st.session_state:
    st.session_state.current_user_id = 'user_analyst_001'  # Default user

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

if 'show_welcome' not in st.session_state:
    st.session_state.show_welcome = True

if 'chat_loaded' not in st.session_state:
    st.session_state.chat_loaded = False

def main():
    """Main application function"""
    
    # Header
    st.markdown('<div class="main-header">🏦 FinKraft Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Unified In-App Assistant for Financial Operations</div>', unsafe_allow_html=True)
    
    # Sidebar - Role Switcher and User Info
    with st.sidebar:
        st.header("⚙️ User Settings")
        
        # Role switcher
        users = st.session_state.data_manager.get_all_users()
        user_options = {f"{user['name']} ({user['role']})": user['id'] for user in users}
        
        selected_user = st.selectbox(
            "Select User Role:",
            options=list(user_options.keys()),
            index=0,
            help="Switch between different user roles to see different permissions"
        )
        
        new_user_id = user_options[selected_user]
        if new_user_id != st.session_state.current_user_id:
            st.session_state.current_user_id = new_user_id
            st.session_state.chat_history = []
            st.session_state.show_welcome = True
            st.session_state.chat_loaded = False  # Reset to load new user's context
            st.rerun()
        
        # Current user info
        current_user = st.session_state.data_manager.get_user_by_id(st.session_state.current_user_id)
        if current_user:
            st.info(f"**Current User:** {current_user['name']}\n**Role:** {current_user['role']}")
        
        st.markdown("---")
        
        # Navigation
        st.header("🧭 Navigation")
        selected_tab = st.radio(
            "Select View:",
            ["💬 Chat", "🔐 Allowed Actions", "📊 Context Pane", "🔍 Trace Viewer"],
            index=0
        )
    
    # Main content area
    if selected_tab == "💬 Chat":
        render_chat_interface()
    elif selected_tab == "🔐 Allowed Actions":
        render_allowed_actions_view()
    elif selected_tab == "📊 Context Pane":
        render_context_pane()
    elif selected_tab == "🔍 Trace Viewer":
        render_trace_viewer()

def load_previous_conversations():
    """Load previous conversation history to show context continuity"""
    # Get recent conversation history from data manager
    conversations = st.session_state.data_manager.get_conversations(st.session_state.current_user_id)
    
    if conversations:
        # Get the most recent conversation
        recent_conv = max(conversations, key=lambda x: x.get('last_updated', ''))
        messages = recent_conv.get('messages', [])
        
        # Clear existing chat history and load all messages from the conversation
        st.session_state.chat_history = []
        for message in messages:  # Load ALL messages, not just last 6
            chat_message = {
                'role': message.get('role'),
                'content': message.get('content'),
                'timestamp': message.get('timestamp'),
                'actions_performed': message.get('actions_performed', []),
                'data_shown': message.get('data_shown', {}),
                'explanation': message.get('explanation', {})
            }
            st.session_state.chat_history.append(chat_message)

def render_chat_interface():
    """Render the main chat interface"""
    
    # Load previous conversation history on first load
    if not st.session_state.chat_loaded:
        load_previous_conversations()
        st.session_state.chat_loaded = True
    
    # Show welcome message on first load
    if st.session_state.show_welcome:
        welcome_response = st.session_state.context_manager.generate_welcome_message(
            st.session_state.current_user_id
        )
        
        if welcome_response.get('show_updates'):
            st.markdown(f'<div class="chat-message context-update">{welcome_response["content"]}</div>', 
                       unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message assistant-message">{welcome_response["content"]}</div>', 
                       unsafe_allow_html=True)
        
        st.session_state.show_welcome = False
    
    # Chat history display
    st.subheader("💬 Conversation")
    
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.markdown(f'<div class="chat-message user-message"><strong>You:</strong> {message["content"]}</div>', 
                           unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-message assistant-message"><strong>Assistant:</strong> {message["content"]}</div>', 
                           unsafe_allow_html=True)
                
                # Show data if available
                if 'data_shown' in message and message['data_shown']:
                    render_message_data(message['data_shown'], message.get('timestamp', ''))
                
                # Show actions performed
                if 'actions_performed' in message and message['actions_performed']:
                    render_actions_performed(message['actions_performed'])
                
                # Show suggested action buttons
                if 'explanation' in message and message['explanation'].get('suggested_action'):
                    render_suggested_actions(message['explanation'])
    
    # Handle pending action from button click
    if 'pending_action' in st.session_state and st.session_state.pending_action:
        user_input = st.session_state.pending_action
        st.session_state.pending_action = None
    else:
        # Chat input
        st.markdown("---")
        user_input = st.chat_input("Type your message here... (e.g., 'Filter invoices for last month, vendor=IndiSky, status=failed')")
    
    if user_input:
        # Get current context
        context = st.session_state.context_manager.get_session_context(st.session_state.current_user_id)
        
        # Process the input
        response = st.session_state.action_processor.process_input(
            user_input, 
            st.session_state.current_user_id, 
            context
        )
        
        # Debug information can be enabled here if needed
        
        # Update context
        if 'context_update' in response:
            st.session_state.context_manager.update_session_context(
                st.session_state.current_user_id, 
                response['context_update']
            )
        
        # Save conversation message
        st.session_state.data_manager.save_conversation_message(
            user_id=st.session_state.current_user_id,
            role='user',
            content=user_input
        )
        
        st.session_state.data_manager.save_conversation_message(
            user_id=st.session_state.current_user_id,
            role='assistant',
            content=response['content'],
            actions_performed=response.get('actions_performed', []),
            data_shown=response.get('data_shown', {}),
            explanation=response.get('explanation', {})
        )
        
        # Refresh conversation history after saving new messages
        load_previous_conversations()
        
        st.rerun()

def render_message_data(data_shown: Dict, timestamp: str = ""):
    """Render data shown in a message"""
    if 'invoices' in data_shown and data_shown['invoices']:
        try:
            st.subheader("📄 Invoice Details")
            
            invoices_df = pd.DataFrame(data_shown['invoices'])
            
            # Format the dataframe for better display - handle different columns dynamically
            available_columns = list(invoices_df.columns)
            
            # Build columns list based on what's actually available
            base_columns = []
            display_columns = []
            
            # Essential columns (check if they exist)
            column_mapping = {
                'invoice_number': 'Invoice #',
                'id': 'Invoice ID',
                'date': 'Date',
                'vendor': 'Vendor',
                'amount': 'Amount',
                'status': 'Status'
            }
            
            for col, display_name in column_mapping.items():
                if col in available_columns:
                    base_columns.append(col)
                    display_columns.append(display_name)
            
            # Add optional columns if they exist and are relevant
            if 'failure_reason' in available_columns and invoices_df['failure_reason'].notna().any():
                base_columns.append('failure_reason')
                display_columns.append('Failure Reason')
            
            if 'payment_terms' in available_columns and any(status in ['pending_approval', 'processed'] for status in invoices_df['status']):
                base_columns.append('payment_terms')
                display_columns.append('Payment Terms')
            
            # Create display dataframe with only available columns
            if base_columns:
                display_df = invoices_df[base_columns].copy()
                
                # Format amount column if it exists
                if 'amount' in display_df.columns:
                    display_df['amount'] = display_df['amount'].apply(lambda x: f"₹{x:,.2f}")
                
                display_df.columns = display_columns
                st.dataframe(display_df, width="stretch")
            else:
                # Fallback: show raw data if no standard columns found
                st.dataframe(invoices_df, width="stretch")
                
            # Summary metrics - dynamic based on invoice statuses
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Invoices", len(data_shown['invoices']))
            with col2:
                st.metric("Total Amount", f"₹{data_shown.get('total_amount', 0):,.2f}")
            with col3:
                # Show relevant metric based on invoice statuses
                statuses = [inv.get('status') for inv in data_shown['invoices']]
                if 'failed' in statuses:
                    failed_count = len([inv for inv in data_shown['invoices'] if inv.get('status') == 'failed'])
                    st.metric("Failed Invoices", failed_count)
                elif 'pending_approval' in statuses:
                    pending_count = len([inv for inv in data_shown['invoices'] if inv.get('status') == 'pending_approval'])
                    st.metric("Pending Approval", pending_count)
                elif 'processed' in statuses:
                    processed_count = len([inv for inv in data_shown['invoices'] if inv.get('status') == 'processed'])
                    st.metric("Processed Invoices", processed_count)
                else:
                    # Show most common status
                    from collections import Counter
                    status_counts = Counter(statuses)
                    if status_counts:
                        most_common_status, count = status_counts.most_common(1)[0]
                        st.metric(f"{most_common_status.replace('_', ' ').title()}", count)
                    else:
                        st.metric("Status", "N/A")
                        
        except Exception as e:
            st.error(f"Error displaying invoice data: {str(e)}")
            st.json(data_shown['invoices'][:2])  # Show first 2 invoices as JSON for debugging
    
    if 'failure_reasons' in data_shown and data_shown['failure_reasons']:
        st.subheader("🚨 Failure Analysis")
        
        reasons_df = pd.DataFrame(list(data_shown['failure_reasons'].items()), 
                                 columns=['Reason', 'Count'])
        
        # Use a unique key based on timestamp to avoid conflicts
        chart_key = f"failure_chart_{timestamp.replace(':', '').replace('-', '').replace('.', '')}"
        fig = px.pie(reasons_df, values='Count', names='Reason', 
                    title="Failure Reasons Distribution")
        st.plotly_chart(fig, width="stretch", key=chart_key)

def render_actions_performed(actions: List[Dict]):
    """Render actions performed by the assistant"""
    st.subheader("⚡ Actions Performed")
    
    for action in actions:
        with st.expander(f"Action: {action.get('action', 'Unknown')}", expanded=False):
            st.json(action)

def render_suggested_actions(explanation: Dict):
    """Render suggested action buttons"""
    if explanation.get('suggested_action') == 'Create support ticket for GSTIN compliance issue':
        st.subheader("✨ Suggested Action")
        
        col1, col2 = st.columns([1, 3])
        with col1:
            # Create unique key using hash of explanation content to avoid duplicates
            # This ensures the same explanation always gets the same key, but different explanations get different keys
            explanation_hash = abs(hash(str(explanation))) % 10000
            unique_key = f"create_ticket_{explanation.get('root_cause', '')}_{explanation_hash}"
            
            if st.button("🎟️ Create Ticket & Notify", type="primary", key=unique_key):
                # Simulate user input for ticket creation
                st.session_state.pending_action = "Create a ticket and notify me when fixed"
                st.rerun()
        
        with col2:
            st.write("**Create support ticket for GSTIN compliance issue**")
            st.caption("This will create a ticket and notify you when the vendor provides updated invoices.")

def render_allowed_actions_view():
    """Render the allowed actions view"""
    st.header("🔐 Allowed Actions")
    st.markdown("*Actions you can perform based on your current role*")
    
    # Get allowed actions for current user
    allowed_actions = st.session_state.data_manager.get_allowed_actions(st.session_state.current_user_id)
    current_user = st.session_state.data_manager.get_user_by_id(st.session_state.current_user_id)
    
    if current_user:
        st.info(f"**Role:** {current_user['role']} | **User:** {current_user['name']}")
    
    if allowed_actions:
        # Group actions by category
        action_categories = {
            'Data Operations': ['filter_invoices', 'analyze_failures', 'view_invoices'],
            'Report Generation': ['generate_report', 'view_financial_summary'],
            'Support & Tickets': ['create_support_ticket', 'view_ticket_status'],
            'Administrative': ['process_payment', 'manage_users', 'system_diagnostics']
        }
        
        for category, category_actions in action_categories.items():
            relevant_actions = [a for a in allowed_actions if a['action'] in category_actions]
            
            if relevant_actions:
                st.subheader(f"📂 {category}")
                
                for action in relevant_actions:
                    with st.expander(f"⚙️ {action['action']}", expanded=False):
                        st.write(f"**Description:** {action['description']}")
                        
                        if action.get('parameters'):
                            st.write("**Parameters:**")
                            for param in action['parameters']:
                                st.write(f"• {param}")
                        
                        if action.get('data_access'):
                            st.write("**Data Access:**")
                            for data_source in action['data_access']:
                                st.write(f"• {data_source}")
                        
                        # Show example usage
                        st.write("**Example Usage:**")
                        if action['action'] == 'filter_invoices':
                            st.code("Filter invoices for last month, vendor='IndiSky', status=failed")
                        elif action['action'] == 'analyze_failures':
                            st.code("Why did these fail?")
                        elif action['action'] == 'create_support_ticket':
                            st.code("Create a ticket and notify me when fixed")
                        elif action['action'] == 'generate_report':
                            st.code("Download the compliance report")
    else:
        st.warning("No actions available for your current role.")

def render_context_pane():
    """Render the context pane showing past requests and open tickets"""
    st.header("📊 Context Pane")
    st.markdown("*Your conversation history and open support tickets*")
    
    # Tabs for different context views
    tab1, tab2, tab3 = st.tabs(["💬 Recent Conversations", "🎟️ Support Tickets", "📈 Quick Stats"])
    
    with tab1:
        st.subheader("Recent Conversations")
        
        # Get conversation history
        history = st.session_state.context_manager.get_conversation_history_for_display(
            st.session_state.current_user_id, limit=20
        )
        
        if history:
            for item in history:
                if item['type'] == 'date_header':
                    st.markdown(f"### 📅 {item['content']}")
                elif item['type'] == 'message':
                    role_emoji = "👤" if item['role'] == 'user' else "🤖"
                    timestamp = item.get('timestamp', '')
                    if timestamp:
                        try:
                            dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                            time_str = dt.strftime('%H:%M')
                        except:
                            time_str = ''
                    else:
                        time_str = ''
                    
                    st.markdown(f"**{role_emoji} {item['role'].title()} {time_str}**")
                    st.markdown(item['content'])
                    
                    if item.get('actions_performed'):
                        with st.expander("View Actions Performed", expanded=False):
                            for action in item['actions_performed']:
                                st.json(action)
                    
                    st.markdown("---")
        else:
            st.info("No conversation history found. Start chatting to see your history here!")
    
    with tab2:
        st.subheader("Support Tickets")
        
        # Get support tickets
        tickets = st.session_state.context_manager.get_active_tickets_for_display(
            st.session_state.current_user_id
        )
        
        if tickets:
            # Filter options
            status_filter = st.selectbox(
                "Filter by Status:",
                options=['All', 'open', 'in_progress', 'resolved'],
                index=0
            )
            
            filtered_tickets = tickets
            if status_filter != 'All':
                filtered_tickets = [t for t in tickets if t['status'] == status_filter]
            
            # Display tickets
            for ticket in filtered_tickets:
                status_color = {
                    'open': '🔓',
                    'in_progress': '🔄', 
                    'resolved': '✅'
                }.get(ticket['status'], '❓')
                
                priority_color = {
                    'high': '🔴',
                    'medium': '🟡',
                    'low': '🟢'
                }.get(ticket['priority'], '⚪')
                
                with st.container():
                    st.markdown(f"""
                    <div class="ticket-card">
                        <h4>{status_color} {ticket['title']} {priority_color}</h4>
                        <p><strong>Ticket ID:</strong> {ticket['id']}</p>
                        <p><strong>Status:</strong> {ticket['status']}</p>
                        <p><strong>Priority:</strong> {ticket['priority']}</p>
                        <p><strong>Created:</strong> {ticket['created_date'][:10]}</p>
                        {f"<p><strong>Resolved:</strong> {ticket['resolved_date'][:10]}</p>" if ticket['resolved_date'] else ""}
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("No support tickets found.")
    
    with tab3:
        st.subheader("Quick Statistics")
        
        # Get some quick stats
        user_context = st.session_state.context_manager.get_user_context(st.session_state.current_user_id)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            open_tickets = len(user_context.get('open_tickets', []))
            st.markdown(f"""
            <div class="metric-card">
                <h3>🎟️</h3>
                <h2>{open_tickets}</h2>
                <p>Open Tickets</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            recent_convs = len(user_context.get('recent_conversations', []))
            st.markdown(f"""
            <div class="metric-card">
                <h3>💬</h3>
                <h2>{recent_convs}</h2>
                <p>Recent Conversations</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            allowed_actions = st.session_state.data_manager.get_allowed_actions(st.session_state.current_user_id)
            action_count = len(allowed_actions)
            st.markdown(f"""
            <div class="metric-card">
                <h3>⚡</h3>
                <h2>{action_count}</h2>
                <p>Available Actions</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            updates = len(user_context.get('recent_updates', []))
            st.markdown(f"""
            <div class="metric-card">
                <h3>📬</h3>
                <h2>{updates}</h2>
                <p>Recent Updates</p>
            </div>
            """, unsafe_allow_html=True)

def render_trace_viewer():
    """Render the trace viewer showing transparency of assistant actions"""
    st.header("🔍 Trace Viewer")
    st.markdown("*See exactly what data was consulted and actions performed*")
    
    if st.session_state.chat_history:
        # Get the most recent assistant messages with actions
        recent_messages = [
            msg for msg in st.session_state.chat_history[-10:] 
            if msg['role'] == 'assistant' and msg.get('actions_performed')
        ]
        
        if recent_messages:
            selected_message = st.selectbox(
                "Select message to trace:",
                options=range(len(recent_messages)),
                format_func=lambda x: f"Message {x+1}: {recent_messages[x]['content'][:50]}..."
            )
            
            message = recent_messages[selected_message]
            
            st.subheader("💬 Message Content")
            st.write(message['content'])
            
            st.subheader("🔬 Trace Details")
            
            # Show actions performed
            if message.get('actions_performed'):
                st.subheader("🔄 Actions Executed")
                
                for i, action in enumerate(message['actions_performed']):
                    with st.expander(f"Action {i+1}: {action.get('action', 'Unknown')}", expanded=True):
                        
                        # Action details
                        st.markdown("**Action Type:**")
                        st.markdown(f'<div class="trace-item">{action.get("action", "Unknown")}</div>', 
                                   unsafe_allow_html=True)
                        
                        # Parameters used
                        if action.get('parameters'):
                            st.markdown("**Parameters:**")
                            st.markdown(f'<div class="trace-item">{json.dumps(action["parameters"], indent=2)}</div>', 
                                       unsafe_allow_html=True)
                        
                        # Data consulted
                        if action.get('data_consulted'):
                            st.markdown("**Data Sources Consulted:**")
                            for source in action['data_consulted']:
                                st.markdown(f'<div class="trace-item">📊 {source}</div>', 
                                           unsafe_allow_html=True)
                        
                        # Results
                        if action.get('results_count') is not None:
                            st.markdown("**Results:**")
                            st.markdown(f'<div class="trace-item">📈 {action["results_count"]} records found</div>', 
                                       unsafe_allow_html=True)
                        
                        # Files generated
                        if action.get('file_generated'):
                            st.markdown("**Files Generated:**")
                            st.markdown(f'<div class="trace-item">📄 {action["file_generated"]}</div>', 
                                       unsafe_allow_html=True)
                        
                        # Ticket created
                        if action.get('ticket_id'):
                            st.markdown("**Support Ticket Created:**")
                            st.markdown(f'<div class="trace-item">🎟️ {action["ticket_id"]}</div>', 
                                       unsafe_allow_html=True)
            
            # Show data that was displayed
            if message.get('data_shown'):
                st.subheader("📈 Data Displayed to User")
                
                data_shown = message['data_shown']
                
                if 'invoice_ids' in data_shown:
                    st.markdown("**Invoice IDs:**")
                    st.markdown(f'<div class="trace-item">{", ".join(data_shown["invoice_ids"])}</div>', 
                               unsafe_allow_html=True)
                
                if 'total_amount' in data_shown:
                    st.markdown("**Total Amount:**")
                    st.markdown(f'<div class="trace-item">₹{data_shown["total_amount"]:,.2f}</div>', 
                               unsafe_allow_html=True)
                
                if 'failure_reasons' in data_shown:
                    st.markdown("**Failure Reasons:**")
                    st.markdown(f'<div class="trace-item">{json.dumps(data_shown["failure_reasons"], indent=2)}</div>', 
                               unsafe_allow_html=True)
            
            # Show explanation provided
            if message.get('explanation'):
                st.subheader("💭 Explanation Provided")
                explanation = message['explanation']
                
                for key, value in explanation.items():
                    st.markdown(f"**{key.replace('_', ' ').title()}:**")
                    st.markdown(f'<div class="trace-item">{value}</div>', 
                               unsafe_allow_html=True)
        else:
            st.info("No traced actions found. Perform some actions in the chat to see traces here.")
    else:
        st.info("No conversation history found. Start chatting to see trace information.")

if __name__ == "__main__":
    main()
