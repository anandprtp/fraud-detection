# Fraud Detection Data Generation 🕵️‍♀️💡

## 📝 Project Overview

This Python project is designed to generate and populate a MySQL database with highly realistic transaction data, specifically tailored for fraud detection and machine learning model training. By simulating complex transaction scenarios, the project provides a robust dataset for developing and testing fraud detection algorithms.

## 📌 Key Features

### ✨ Massive Scale Data Generation
- Generates over 100,000 synthetic transactions
- Creates comprehensive customer and merchant profiles
- Simulates diverse transaction scenarios

### 🕵️ Advanced Fraud Simulation
- Generates both legitimate and fraudulent transactions
- Implements nuanced fraud patterns
- Supports anomaly detection research and model training

### 💾 Optimized Database Performance
- Utilizes bulk insertion techniques
- Maintains referential integrity
- Efficient database schema design

## 🛠 Technology Stack

### Languages & Libraries
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
- **Libraries:**
  - Faker: Synthetic data generation
  - NumPy: Numerical computing
  - Pandas: Data manipulation
  - mysql-connector-python: Database interaction
  - tqdm: Progress tracking

### Database
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white)
- Relational database management
- Structured transaction storage
- Complex query support

### Development Tools
![Git](https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white)
![PyCharm](https://img.shields.io/badge/PyCharm-000000?style=flat-square&logo=pycharm&logoColor=white)
- Version Control: Git & GitHub
- IDE: PyCharm (Primary Development Environment)

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.8+
- MySQL 8.0+
- Git

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/anandprtp/fraud-detection.git
   cd fraud-detection
   ```

2. **Create Virtual Environment (Optional but Recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Database**
   Update `config.py` with your database credentials:
   ```python
   DB_CONFIG = {
       'host': 'localhost',
       'user': 'your_username',
       'password': 'your_password',
       'database': 'fraud_detection_db'
   }
   ```

5. **Generate Data**
   ```bash
   python generate_data.py
   ```

## 🔍 Project Structure
```
fraud-detection/
│
├── .idea/                     # PyCharm project configuration
├── inspectionProfiles/        # IDE inspection profile settings
├── .gitignore                 # Git ignore configuration
├── generate_data.py           # Main data generation script
└── ... (other project files)
```

## 📊 Data Generation Details
- **Transactions:** 100,000+ records
- **Customer Profiles:** Realistic personal information
- **Merchant Categories:** Diverse business types
- **Transaction Types:**
  - Regular purchases
  - High-risk transactions
  - Anomalous patterns

## 🤝 Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📜 License
MIT License - Feel free to use and modify

## 🌟 Support
If you find this project helpful, please consider:
- Starring the repository
- Sharing with your network
- Reporting issues or providing feedback through GitHub Issues

---

**🐞 Feedback Welcome!**
*Contributions, suggestions, and feedback are always appreciated!*
