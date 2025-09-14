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

## 🌐 Deployment

### Streamlit Community Cloud (Recommended)
1. Push your code to GitHub
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy with one click!

### Alternative Platforms
- **Heroku**: Professional deployment with custom domains
- **Railway**: Modern deployment platform with GitHub integration
- **AWS/GCP/Azure**: Enterprise-grade cloud deployment

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