Fraud Detection Data Generation 🕵️‍♀️💡

📝 Project Overview
This Python project is designed to generate and populate a MySQL database with highly realistic transaction data, specifically tailored for fraud detection and machine learning model training. By simulating complex transaction scenarios, the project provides a robust dataset for developing and testing fraud detection algorithms.
📌 Key Features
✨ Massive Scale Data Generation

Generates over 100,000 synthetic transactions
Creates comprehensive customer and merchant profiles
Simulates diverse transaction scenarios

🕵️ Advanced Fraud Simulation

Generates both legitimate and fraudulent transactions
Implements nuanced fraud patterns
Supports anomaly detection research and model training

💾 Optimized Database Performance

Utilizes bulk insertion techniques
Maintains referential integrity
Efficient database schema design

🛠 Technology Stack
Languages & Libraries

Python

Faker: Synthetic data generation
NumPy: Numerical computing
Pandas: Data manipulation
mysql-connector-python: Database interaction
tqdm: Progress tracking


Database

MySQL

Relational database management
Structured transaction storage
Complex query support


Development Tools

Version Control: Git & GitHub
IDE: VS Code, PyCharm (recommended)

🚀 Quick Start Guide
Prerequisites

Python 3.8+
MySQL 8.0+
Git

Installation Steps

Clone the Repository
bashCopygit clone https://github.com/YourGitHubUsername/fraud-detection.git
cd fraud-detection

Create Virtual Environment (Optional but Recommended)
bashCopypython -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install Dependencies
bashCopypip install -r requirements.txt

Configure Database

Create a MySQL database
Update config.py with your database credentials

pythonCopyDB_CONFIG = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'fraud_detection_db'
}

Generate Data
bashCopypython generate_data.py


🔍 Project Structure
fraud-detection/
│
├── .idea/                     # PyCharm project configuration
│   ├── inspectionProfiles/    # IDE inspection profile settings
│   ├── .gitignore             # Git ignore configuration
│   ├── Financial Fraud Detection.iml  # IntelliJ module file
│   ├── misc.xml               # Miscellaneous IDE settings
│   └── modules.xml            # Project modules configuration
│
└── generate_data.py           # Main data generation script

📊 Data Generation Details

Transactions: 100,000+ records
Customer Profiles: Realistic personal information
Merchant Categories: Diverse business types
Transaction Types:

Regular purchases
High-risk transactions
Anomalous patterns


🤝 Contributing

Fork the repository
Create a feature branch
Commit your changes
Push to the branch
Create a Pull Request

📜 License
MIT License - Feel free to use and modify
🌟 Star the Repository
If you find this project helpful, please consider starring the repository!
🐞 Issues & Feedback
Report issues or provide feedback through GitHub Issues.