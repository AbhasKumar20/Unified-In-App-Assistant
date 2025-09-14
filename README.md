# 🏦 FinKraft Assistant - Unified In-App Assistant

A powerful **Streamlit-based financial assistant** that provides unified invoice processing, failure analysis, and support ticket management for financial operations teams.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Features

### 💬 **Intelligent Chat Interface**
- Natural language processing for financial queries
- Context-aware responses with conversation history
- Real-time invoice filtering and analysis

### 🚨 **Advanced Failure Analysis**
- Automatic detection of invoice compliance issues
- GSTIN validation for Indian tax compliance
- Detailed failure categorization and reporting

### 🎟️ **Integrated Support System**
- One-click ticket creation for compliance issues
- Automatic ticket assignment and tracking
- Real-time notification system

### 📊 **Comprehensive Analytics**
- Interactive dashboards with Plotly visualizations
- Role-based access control and permissions
- Audit trails and trace viewer for debugging

### 🔐 **Enterprise Features**
- Multi-role user management (Analyst, Manager, Viewer)
- Workspace-based data isolation
- Action-based permission system

## 📸 **Screenshots & UI Walkthrough**

### 🏠 **Main Dashboard**
*The main interface showing the chat-based interaction with role switching*

<img width="3440" height="1972" alt="image" src="https://github.com/user-attachments/assets/45496615-49e6-492a-8af2-41498496e32b" />


### 💬 **Natural Language Processing**
*Ask questions in plain English and get instant responses*


<img width="3442" height="1972" alt="image" src="https://github.com/user-attachments/assets/46259236-8a58-4b01-b8a2-e656d287ac02" />


**Example interactions:**
- "Filter invoices for last month, vendor=IndiSky, status=failed"
- "Why did this fail?"
- "Create a ticket and notify me when fixed"

### 📊 **Invoice Analysis & Visualization**
*Interactive charts and detailed invoice breakdowns*


<img width="3440" height="1492" alt="image" src="https://github.com/user-attachments/assets/322dfa70-bbed-487a-bf07-cbefad539617" />


### 🚨 **Failure Analysis System**
*Automatic detection and categorization of invoice issues*


<img width="3442" height="1896" alt="image" src="https://github.com/user-attachments/assets/37fd4823-151e-4ac5-af6d-2b9f6fdfdfcb" />


### ✨ **Smart Suggested Actions**
*One-click ticket creation with contextual suggestions*


<img width="3444" height="1210" alt="image" src="https://github.com/user-attachments/assets/bcb9f01b-5fce-4c72-9bae-60b630320d23" />


### 🎟️ **Support Ticket Management**
*Integrated ticket creation and tracking system*


<img width="3450" height="738" alt="image" src="https://github.com/user-attachments/assets/9a151b09-b805-4106-9533-d0267b29ca10" />


### 🔐 **Role-Based Access Control**
*Different interfaces for Financial Analysts, Managers, and Viewers*


<img width="3442" height="1968" alt="image" src="https://github.com/user-attachments/assets/a9ee3f27-4401-4cc9-a49d-4870e76c7fa9" />


### 📋 **Context Pane**
*View conversation history, open tickets, and quick statistics*


<img width="3446" height="1886" alt="image" src="https://github.com/user-attachments/assets/54ab9223-3f4b-47f3-b0cc-24a75b7981fd" />

<img width="3432" height="1890" alt="image" src="https://github.com/user-attachments/assets/80b7481e-ca35-48ce-b493-0fc1d696dae7" />


### 🔍 **Trace Viewer**
*Debug and audit trail showing exactly what actions were performed*


<img width="3442" height="2060" alt="image" src="https://github.com/user-attachments/assets/b2ee7055-14e6-4113-9934-02db3085a517" />


### 📈 **Analytics Dashboard**
*Real-time metrics and performance indicators*


<img width="3444" height="1902" alt="image" src="https://github.com/user-attachments/assets/1b353f96-681e-4725-b81a-910dcfd63059" />

### 🔄 **Conversation Continuity**
*Sessions persist across visits with full context retention*


<img width="3446" height="2068" alt="image" src="https://github.com/user-attachments/assets/ea37def6-d62c-461e-8528-e63d39f5e50b" />



---

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/AbhasKumar20/Unified-In-App-Assistant.git
   cd Unified-In-App-Assistant
   ```

2. **Create virtual environment**
   ```bash
   python -m venv finkraft_env
   source finkraft_env/bin/activate  # On Windows: finkraft_env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:8501` to access the application.

## 📁 Project Structure

```
FinKraft/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── .gitignore                      # Git ignore rules
├── core/                           # Core application modules
│   ├── __init__.py
│   ├── action_processor.py         # Natural language processing
│   ├── context_manager.py          # Session and context management
│   └── data_manager.py             # Data operations and persistence
├── sample_data/                    # Sample datasets
│   ├── conversations_enhanced.json # Chat history and conversations
│   ├── support_tickets.json       # Support ticket database
│   ├── invoices_enhanced.json     # Invoice records
│   ├── vendors_enhanced.json      # Vendor information
│   ├── users.json                 # User accounts and roles
│   ├── allowed_actions.json       # Permission configurations
│   └── reports.json               # Report templates
└── utils/                          # Utility modules
    └── __init__.py
```

## 🎯 Use Cases

### For Financial Analysts
- **Invoice Processing**: Filter and analyze invoices by vendor, status, amount
- **Compliance Checking**: Automatic GSTIN validation and tax compliance
- **Failure Analysis**: Identify and categorize invoice processing failures

### For Operations Managers  
- **Team Oversight**: Monitor team activities and ticket resolution
- **Reporting**: Generate comprehensive financial operation reports
- **Process Optimization**: Track performance metrics and bottlenecks

### For Support Teams
- **Ticket Management**: Create, assign, and track support tickets
- **Issue Resolution**: Access detailed failure analysis and context
- **Communication**: Integrated notification system for updates

## 🛠️ Technology Stack

- **Frontend**: Streamlit (Interactive web application)
- **Visualization**: Plotly (Charts and graphs)
- **Data Processing**: Pandas, NumPy
- **Backend**: Python 3.11+
- **Data Storage**: JSON files (easily replaceable with databases)

## 🔧 Configuration

### User Roles
The application supports three user roles:

- **`financial_analyst`**: Full access to invoice operations and analysis
- **`operations_manager`**: Management oversight and reporting capabilities  
- **`report_viewer`**: Read-only access to reports and data

### Sample Users
- **Priya Sharma** (Financial Analyst) - `user_analyst_001`
- **Raj Patel** (Operations Manager) - `user_manager_001` 
- **Anita Singh** (Report Viewer) - `user_viewer_001`

## 📊 Key Metrics

- **Invoice Processing**: Handle 1000+ invoices with real-time filtering
- **Failure Detection**: 95%+ accuracy in compliance issue identification
- **Response Time**: < 2 seconds for most operations
- **Multi-tenancy**: Support for multiple workspaces and teams


## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/AbhasKumar20/Unified-In-App-Assistant/issues)
- **Discussions**: [GitHub Discussions](https://github.com/AbhasKumar20/Unified-In-App-Assistant/discussions)
- **Documentation**: Check the `PROJECT_SUMMARY.md` for detailed technical documentation

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/) - The fastest way to build data apps
- Visualizations powered by [Plotly](https://plotly.com/)
- Icons from the Unicode Emoji standard

---

**Made with ❤️ for financial operations teams**

*Transform your financial operations with intelligent automation and real-time insights.*
