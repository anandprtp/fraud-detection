import mysql.connector
import random
from faker import Faker
from datetime import datetime, timedelta
import time
import numpy as np
import math
from tqdm import tqdm

# Initialize Faker
fake = Faker()
Faker.seed(42)  # For reproducibility
random.seed(42)
np.random.seed(42)

# Database connection
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Replace with your username
            password="Manu@7017",  # Replace with your password
            database="fraud_detection"  # Replace with your database name
        )
        return connection
    except mysql.connector.Error as error:
        print(f"Error connecting to MySQL: {error}")
        try:
            # Create database if it doesn't exist
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="password"
            )
            cursor = conn.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS fraud_detection")
            conn.commit()
            conn.close()

            # Connect to the newly created database
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="password",
                database="fraud_detection"
            )

            # # Create tables
            # create_tables(connection)

            return connection
        except mysql.connector.Error as error:
            print(f"Failed to create database: {error}")
            return None

# Create tables if they don't exist
# def create_tables(connection):
#     cursor = connection.cursor()
#
#     # Customers table
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS Customers (
#         customer_id INT AUTO_INCREMENT PRIMARY KEY,
#         first_name VARCHAR(50) NOT NULL,
#         last_name VARCHAR(50) NOT NULL,
#         email VARCHAR(100) NOT NULL,
#         phone_number VARCHAR(20),
#         date_of_birth DATE,
#         gender CHAR(1),
#         country VARCHAR(50),
#         city VARCHAR(50),
#         zip_code VARCHAR(20),
#         account_open_date DATE,
#         account_status VARCHAR(20),
#         annual_income DECIMAL(12, 2),
#         credit_score INT,
#         risk_level VARCHAR(10),
#         employment_status VARCHAR(20),
#         customer_segment VARCHAR(50),
#         linked_accounts INT
#     )
#     """)
#
#     # Merchants table
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS Merchants (
#         merchant_id INT AUTO_INCREMENT PRIMARY KEY,
#         merchant_name VARCHAR(100) NOT NULL,
#         merchant_category VARCHAR(50),
#         country VARCHAR(50),
#         city VARCHAR(50),
#         zip_code VARCHAR(20),
#         merchant_risk_score INT,
#         fraudulent_flag BOOLEAN,
#         transaction_volume INT
#     )
#     """)
#
#     # Transactions table
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS Transactions (
#         transaction_id INT AUTO_INCREMENT PRIMARY KEY,
#         customer_id INT,
#         merchant_id INT,
#         transaction_date DATETIME,
#         transaction_amount DECIMAL(12, 2),
#         currency VARCHAR(3),
#         transaction_type VARCHAR(20),
#         device_used VARCHAR(20),
#         location_lat DECIMAL(10, 7),
#         location_long DECIMAL(10, 7),
#         is_fraud BOOLEAN,
#         transaction_status VARCHAR(20),
#         masked_card_number VARCHAR(20),
#         card_expiry_date DATE,
#         ip_address VARCHAR(15),
#         authentication_method VARCHAR(20),
#         previous_transaction_time DATETIME,
#         time_since_last_transaction INT,
#         unusual_timing_flag BOOLEAN,
#         distance_from_home DECIMAL(10, 2),
#         FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
#         FOREIGN KEY (merchant_id) REFERENCES Merchants(merchant_id)
#     )
#     """)
#
#     # Fraud Cases table
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS FraudCases (
#         case_id INT AUTO_INCREMENT PRIMARY KEY,
#         transaction_id INT,
#         fraud_reason VARCHAR(100),
#         reported_by VARCHAR(20),
#         resolution_status VARCHAR(20),
#         fraud_probability_score DECIMAL(5, 2),
#         investigator_comments TEXT,
#         reported_date DATETIME,
#         resolved_date DATETIME,
#         financial_impact DECIMAL(12, 2),
#         recovery_amount DECIMAL(12, 2),
#         recovery_status VARCHAR(20),
#         recovery_method VARCHAR(50),
#         case_priority VARCHAR(10),
#         FOREIGN KEY (transaction_id) REFERENCES Transactions(transaction_id)
#     )
#     """)
#
#     connection.commit()

# Generate random customers
from datetime import datetime  # Ensure this import is at the top of your script


def generate_customers(num_customers=10000):
    customers = []

    # Define date range using datetime objects
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2024, 12, 31)

    # Generate different customer segments with realistic distributions
    segments = [
        'High Net Worth', 'Student', 'Frequent Traveler', 'Senior Citizen',
        'Business Owner', 'Low-Income Individual', 'Tech-Savvy Shopper', 'New Customer'
    ]
    segment_weights = [0.05, 0.15, 0.1, 0.1, 0.08, 0.2, 0.22, 0.1]

    # Risk level distribution (most customers should be low risk)
    risk_levels = ['low', 'medium', 'high']
    risk_weights = [0.7, 0.2, 0.1]

    # Employment status options
    employment_statuses = ['Employed', 'Self-employed', 'Unemployed', 'Student', 'Retired']

    # Create anomalous customers (5% of the total)
    num_anomalous = int(num_customers * 0.05)
    anomalous_indices = set(random.sample(range(num_customers), num_anomalous))

    print("Generating customers...")
    for i in tqdm(range(num_customers)):
        is_anomalous = i in anomalous_indices

        dob = fake.date_of_birth(minimum_age=18, maximum_age=90)
        gender = random.choice(['M', 'F', 'O'])

        # Assign realistic income based on customer segment
        segment = random.choices(segments, weights=segment_weights)[0]

        if segment == 'High Net Worth':
            annual_income = random.uniform(150000, 1000000)
            credit_score = random.randint(700, 850)
        elif segment == 'Student':
            annual_income = random.uniform(5000, 30000)
            credit_score = random.randint(300, 700)
        elif segment == 'Low-Income Individual':
            annual_income = random.uniform(15000, 40000)
            credit_score = random.randint(400, 700)
        else:
            annual_income = random.uniform(35000, 150000)
            credit_score = random.randint(500, 800)

        # Create anomalies in some customers
        if is_anomalous:
            # Anomaly: extremely high income with low credit score
            if random.random() < 0.3:
                annual_income = random.uniform(500000, 5000000)
                credit_score = random.randint(300, 450)

            # Anomaly: newly created account with high risk
            if random.random() < 0.4:
                account_open_date = fake.date_between(start_date=datetime(2023, 10, 1), end_date=end_date)
                risk_level = 'high'
            else:
                account_open_date = fake.date_between(start_date=start_date, end_date=end_date)

                # Assign risk level with some correlation to credit score
                if credit_score < 550:
                    risk_level_choices = ['medium', 'high']
                    risk_level_weights = [0.4, 0.6]
                elif credit_score < 680:
                    risk_level_choices = ['low', 'medium', 'high']
                    risk_level_weights = [0.3, 0.5, 0.2]
                else:
                    risk_level_choices = ['low', 'medium', 'high']
                    risk_level_weights = [0.8, 0.15, 0.05]

                risk_level = random.choices(risk_level_choices, weights=risk_level_weights)[0]
        else:
            account_open_date = fake.date_between(start_date=start_date, end_date=end_date)

            # Assign risk level with some correlation to credit score
            if credit_score < 550:
                risk_level_choices = ['medium', 'high']
                risk_level_weights = [0.4, 0.6]
            elif credit_score < 680:
                risk_level_choices = ['low', 'medium', 'high']
                risk_level_weights = [0.3, 0.5, 0.2]
            else:
                risk_level_choices = ['low', 'medium', 'high']
                risk_level_weights = [0.8, 0.15, 0.05]

            risk_level = random.choices(risk_level_choices, weights=risk_level_weights)[0]

        # Generate employment status with some correlation to income and age
        if dob.year > 2000:  # Younger customers
            employment_status_weights = [0.4, 0.1, 0.1, 0.4, 0]
        elif dob.year > 1960:  # Middle-aged
            employment_status_weights = [0.65, 0.2, 0.1, 0.05, 0]
        else:  # Older customers
            employment_status_weights = [0.2, 0.1, 0.05, 0, 0.65]

        employment_status = random.choices(employment_statuses, weights=employment_status_weights)[0]

        # Account status (most should be active)
        account_status = random.choices(['active', 'closed', 'suspended'], weights=[0.9, 0.08, 0.02])[0]

        # Anomaly: Many linked accounts for high-risk customers
        linked_accounts = random.randint(1, 5)
        if is_anomalous and risk_level == 'high':
            linked_accounts = random.randint(10, 20)

        # Generate phone number and truncate it to 20 characters
        phone_number = fake.phone_number()[:20]

        customer = {
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'phone_number': phone_number,  # Truncated phone number
            'date_of_birth': dob.strftime('%Y-%m-%d'),
            'gender': gender,
            'country': fake.country(),
            'city': fake.city(),
            'zip_code': fake.zipcode(),
            'account_open_date': account_open_date.strftime('%Y-%m-%d'),
            'account_status': account_status,
            'annual_income': annual_income,
            'credit_score': credit_score,
            'risk_level': risk_level,
            'employment_status': employment_status,
            'customer_segment': segment,
            'linked_accounts': linked_accounts
        }
        customers.append(customer)

    return customers

# Generate random merchants
def generate_merchants(num_merchants=2000):
    merchants = []

    # Merchant categories with realistic distribution
    categories = [
        'Retail', 'Food & Dining', 'Travel', 'Entertainment', 'Services',
        'Healthcare', 'Technology', 'Financial Services', 'Education',
        'Gambling', 'Dating Services', 'Cryptocurrency'  # Higher risk categories
    ]
    category_weights = [0.2, 0.18, 0.12, 0.1, 0.15, 0.08, 0.07, 0.05, 0.03, 0.007, 0.003, 0.01]

    # Countries with realistic distribution
    countries = ['United States', 'Canada', 'United Kingdom', 'Germany', 'France',
                'Japan', 'Australia', 'China', 'India', 'Brazil', 'Mexico', 'Nigeria']
    country_weights = [0.3, 0.1, 0.1, 0.08, 0.08, 0.07, 0.05, 0.07, 0.05, 0.05, 0.03, 0.02]

    # Create anomalous merchants (3% of the total)
    num_anomalous = int(num_merchants * 0.03)
    anomalous_indices = set(random.sample(range(num_merchants), num_anomalous))

    print("Generating merchants...")
    for i in tqdm(range(num_merchants)):
        is_anomalous = i in anomalous_indices

        if is_anomalous:
            # Anomalous merchants are more likely to be in high-risk categories
            category = random.choices(['Gambling', 'Dating Services', 'Cryptocurrency'], weights=[0.4, 0.3, 0.3])[0]
            risk_score = random.randint(8, 10)
            fraudulent_flag = random.choices([0, 1], weights=[0.5, 0.5])[0]

            # Anomaly: extremely high transaction volume
            transaction_volume = random.randint(500000, 2000000)
        else:
            category = random.choices(categories, weights=category_weights)[0]
            country = random.choices(countries, weights=country_weights)[0]

            # Assign merchant risk score - higher for certain categories
            if category in ['Gambling', 'Dating Services', 'Cryptocurrency']:
                risk_score = random.randint(6, 10)
                fraudulent_flag = random.choices([0, 1], weights=[0.9, 0.1])[0]
            else:
                risk_score = random.randint(1, 5)
                fraudulent_flag = random.choices([0, 1], weights=[0.99, 0.01])[0]

            transaction_volume = random.randint(10, 100000)

        country = random.choices(countries, weights=country_weights)[0]

        merchant = {
            'merchant_name': fake.company(),
            'merchant_category': category,
            'country': country,
            'city': fake.city(),
            'zip_code': fake.zipcode(),
            'merchant_risk_score': risk_score,
            'fraudulent_flag': fraudulent_flag,
            'transaction_volume': transaction_volume
        }
        merchants.append(merchant)

    return merchants

# Generate random transactions
def generate_transactions(num_transactions, customer_ids, merchant_ids):
    transactions = []

    # Transaction types with distribution
    transaction_types = ['online', 'POS', 'ATM', 'contactless']
    transaction_type_weights = [0.4, 0.3, 0.1, 0.2]

    # Device distribution
    devices = {
        'online': ['mobile', 'desktop'],
        'POS': ['POS terminal'],
        'ATM': ['ATM terminal'],
        'contactless': ['mobile', 'POS terminal']
    }

    # Transaction status distribution
    statuses = ['approved', 'declined', 'pending']
    status_weights = [0.95, 0.04, 0.01]

    # Authentication methods
    auth_methods = {
        'online': ['3D secure', 'none'],
        'POS': ['PIN', 'signature'],
        'ATM': ['PIN'],
        'contactless': ['PIN', 'none']
    }

    # Currencies with distribution
    currencies = ['USD', 'EUR', 'GBP', 'CAD', 'JPY', 'AUD']
    currency_weights = [0.6, 0.15, 0.1, 0.05, 0.05, 0.05]

    # Time of day distribution (transactions more likely during daytime)
    hour_weights = [
        0.01, 0.005, 0.005, 0.005, 0.01, 0.02,  # 0-5 AM
        0.03, 0.05, 0.06, 0.07, 0.08, 0.09,  # 6-11 AM
        0.1, 0.1, 0.09, 0.08, 0.07, 0.06,  # 12-5 PM
        0.07, 0.08, 0.06, 0.04, 0.03, 0.02  # 6-11 PM
    ]

    # Track last transaction times for each customer
    last_transaction_times = {}

    # Store customer home locations
    customer_locations = {}
    for customer_id in customer_ids:
        customer_locations[customer_id] = (
            float(fake.latitude()),
            float(fake.longitude())
        )

    # Create a small percentage of fraudulent transactions (0.3% by default)
    is_fraud_weights = [0.997, 0.003]  # 0.3% fraud rate

    # Generate anomalous transactions (5% of total)
    num_anomalous = int(num_transactions * 0.05)
    anomalous_indices = set(random.sample(range(num_transactions), num_anomalous))

    # Generate transaction dates within 2022-01-01 to 2024-12-31
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2024, 12, 31)

    print("Generating transactions...")

    for i in tqdm(range(num_transactions)):
        is_anomalous = i in anomalous_indices

        # Use valid customer_id and merchant_id
        customer_id = random.choice(customer_ids)
        merchant_id = random.choice(merchant_ids)

        # Generate realistic transaction date
        transaction_date = fake.date_time_between(start_date=start_date, end_date=end_date)

        # Adjust hour based on distribution
        hour = random.choices(range(24), weights=hour_weights)[0]
        transaction_date = transaction_date.replace(hour=hour)

        # Generate transaction amount based on customer ID (consistent spending patterns)
        mean_amount = 10 + (customer_id % 100) * 5  # Different customers have different spending patterns
        if customer_id % 10 == 0:  # Some customers make larger transactions
            mean_amount *= 10

        # Create anomalous transaction amounts for anomalous transactions
        if is_anomalous:
            if random.random() < 0.7:
                # Very large transaction amount
                transaction_amount = round(random.uniform(10000, 50000), 2)
            else:
                # Unusual precise amount (often associated with fraud)
                transaction_amount = round(random.uniform(1000, 5000) + random.uniform(0.01, 0.99), 2)
        else:
            # Log-normal distribution for transaction amounts
            transaction_amount = round(random.lognormvariate(math.log(mean_amount), 0.8), 2)

        # Select transaction type
        transaction_type = random.choices(transaction_types, weights=transaction_type_weights)[0]

        # Select device based on transaction type
        device_options = devices[transaction_type]
        device_used = random.choice(device_options)

        # Select currency
        currency = random.choices(currencies, weights=currency_weights)[0]

        # Select authentication method based on transaction type
        auth_options = auth_methods[transaction_type]
        authentication_method = random.choice(auth_options)

        # Generate transaction location (somewhat close to customer home location)
        home_lat, home_long = customer_locations[customer_id]

        # Different location patterns for anomalous transactions
        if is_anomalous:
            # Far from home (high chance of fraud)
            location_lat = home_lat + random.uniform(-10, 10)
            location_long = home_long + random.uniform(-10, 10)
            distance_from_home = random.uniform(500, 5000)  # 500-5000 km
        else:
            # Most transactions happen near home
            if random.random() < 0.8:
                # Near home
                location_lat = home_lat + random.uniform(-0.05, 0.05)
                location_long = home_long + random.uniform(-0.05, 0.05)
                distance_from_home = random.uniform(0, 10)  # 0-10 km
            else:
                # Far from home
                location_lat = home_lat + random.uniform(-5, 5)
                location_long = home_long + random.uniform(-5, 5)
                distance_from_home = random.uniform(20, 1000)  # 20-1000 km

        # Calculate time since last transaction
        previous_transaction_time = None
        time_since_last_transaction = None

        if customer_id in last_transaction_times:
            previous_transaction_time = last_transaction_times[customer_id]
            time_diff = transaction_date - previous_transaction_time
            time_since_last_transaction = int(time_diff.total_seconds())

        last_transaction_times[customer_id] = transaction_date

        # Determine if unusual timing
        unusual_timing_flag = 0

        # Anomalous transactions often have unusual timing
        if is_anomalous:
            if time_since_last_transaction is not None and time_since_last_transaction < 60:  # Less than 1 minute
                unusual_timing_flag = 1
        else:
            if time_since_last_transaction is not None and time_since_last_transaction < 300 and distance_from_home > 20:
                unusual_timing_flag = 1

        # Generate masked card number
        masked_card_number = f"{''.join(random.choices('0123456789', k=4))}-XXXX-XXXX-{''.join(random.choices('0123456789', k=4))}"

        # Generate card expiry date
        expiry_year = random.randint(datetime.now().year, datetime.now().year + 5)
        expiry_month = random.randint(1, 12)
        expiry_date = f"{expiry_year}-{expiry_month:02d}-01"

        # Generate IP address for online transactions
        ip_address = None
        if transaction_type == 'online':
            ip_address = fake.ipv4()

        # Make fraud more likely based on certain conditions
        if unusual_timing_flag == 1:
            is_fraud = random.choices([0, 1], weights=[0.7, 0.3])[0]

        # Make fraud more likely for certain authentication methods
        if authentication_method == 'none':
            is_fraud = random.choices([0, 1], weights=[0.9, 0.1])[0]

        # Make fraud more likely for high-amount transactions
        if transaction_amount > 1000:
            is_fraud = random.choices([0, 1], weights=[0.95, 0.05])[0]

        # Status is more likely to be declined if it's fraud
        if is_fraud == 1:
            transaction_status = random.choices(statuses, weights=[0.3, 0.65, 0.05])[0]
        else:
            transaction_status = random.choices(statuses, weights=status_weights)[0]

        transaction = {
            'customer_id': customer_id,
            'merchant_id': merchant_id,
            'transaction_date': transaction_date.strftime('%Y-%m-%d %H:%M:%S'),
            'transaction_amount': transaction_amount,
            'currency': currency,
            'transaction_type': transaction_type,
            'device_used': device_used,
            'location_lat': location_lat,
            'location_long': location_long,
            'is_fraud': is_fraud,
            'transaction_status': transaction_status,
            'masked_card_number': masked_card_number,
            'card_expiry_date': expiry_date,
            'ip_address': ip_address,
            'authentication_method': authentication_method,
            'previous_transaction_time': previous_transaction_time.strftime(
                '%Y-%m-%d %H:%M:%S') if previous_transaction_time else None,
            'time_since_last_transaction': time_since_last_transaction,
            'unusual_timing_flag': unusual_timing_flag,
            'distance_from_home': distance_from_home
        }

        transactions.append(transaction)

    return transactions

# Generate fraud cases for fraudulent transactions
def generate_fraud_cases(transactions):
    fraud_cases = []

    fraud_reasons = [
        "Suspicious transaction location",
        "Unusual transaction amount",
        "Multiple transactions in short timeframe",
        "Transaction at unusual time of day",
        "Transaction with known fraudulent merchant",
        "Card reported stolen",
        "Suspicious IP address",
        "Failed authentication attempts",
        "Transaction from unusual device",
        "Unusual spending pattern"
    ]

    reported_by_options = ['customer', 'system', 'bank', 'merchant']
    reported_by_weights = [0.3, 0.5, 0.15, 0.05]

    resolution_status_options = ['pending', 'resolved', 'escalated']
    resolution_status_weights = [0.4, 0.5, 0.1]

    recovery_status_options = ['not started', 'in progress', 'partial', 'full', 'written off']
    recovery_status_weights = [0.2, 0.3, 0.2, 0.2, 0.1]

    recovery_methods = [
        "Chargeback",
        "Customer reimbursement",
        "Merchant refund",
        "Insurance claim",
        "Legal action",
        "Write-off"
    ]

    case_priority_options = ['low', 'medium', 'high', 'critical']

    print("Generating fraud cases...")
    for transaction in tqdm([t for t in transactions if t['is_fraud'] == 1]):
        # Random delay between transaction and fraud reporting
        transaction_date = datetime.strptime(transaction['transaction_date'], '%Y-%m-%d %H:%M:%S')
        report_delay = random.randint(1, 30)  # 1-30 days
        reported_date = transaction_date + timedelta(days=report_delay)

        # Ensure reported date is not after end_date (2024-12-31)
        end_date = datetime(2024, 12, 31)
        if reported_date > end_date:
            reported_date = end_date

        # Some cases get resolved
        is_resolved = random.random() < 0.7
        resolved_date = None
        if is_resolved:
            resolution_delay = random.randint(1, 60)  # 1-60 days to resolve
            resolved_date = reported_date + timedelta(days=resolution_delay)

            # Ensure resolved date is not after end_date (2024-12-31)
            if resolved_date > end_date:
                resolved_date = end_date

        # Select resolution status
        if is_resolved:
            resolution_status = 'resolved'
        else:
            resolution_status = random.choices(['pending', 'escalated'], weights=[0.7, 0.3])[0]

        # Select fraud reason
        fraud_reason = random.choice(fraud_reasons)

        # Determine fraud probability score
        if resolution_status == 'resolved':
            fraud_probability_score = random.uniform(70, 100)
        else:
            fraud_probability_score = random.uniform(40, 95)

        # Determine financial impact (usually close to transaction amount)
        transaction_amount = transaction['transaction_amount']
        financial_impact = transaction_amount * random.uniform(0.9, 1.1)

        # Determine recovery amount
        if resolution_status == 'resolved':
            recovery_percent = random.uniform(0.7, 1.0)
        else:
            recovery_percent = random.uniform(0, 0.3)

        recovery_amount = financial_impact * recovery_percent

        # Select recovery status
        if recovery_amount < 0.1:
            recovery_status = 'not started'
        elif recovery_amount < financial_impact * 0.5:
            recovery_status = random.choice(['in progress', 'partial'])
        elif recovery_amount >= financial_impact * 0.9:
            recovery_status = 'full'
        else:
            recovery_status = random.choice(recovery_status_options)

        # Select recovery method
        recovery_method = random.choice(recovery_methods)

        # Select case priority
        if financial_impact > 10000:
            case_priority = 'critical'
        elif financial_impact > 1000:
            case_priority = 'high'
        elif financial_impact > 100:
            case_priority = 'medium'
        else:
            case_priority = 'low'

        # Generate investigator comments
        if resolution_status == 'resolved':
            investigator_comments = f"Case resolved. {recovery_status.capitalize()} recovery through {recovery_method}."
        elif resolution_status == 'escalated':
            investigator_comments = f"Case escalated due to complexity. Working with {random.choice(['fraud team', 'legal', 'customer service'])}."
        else:
            investigator_comments = f"Investigation ongoing. Initial assessment: {fraud_reason}."

        fraud_case = {
            'transaction_id': None,  # Will be set after transaction is inserted
            'fraud_reason': fraud_reason,
            'reported_by': random.choices(reported_by_options, weights=reported_by_weights)[0],
            'resolution_status': resolution_status,
            'fraud_probability_score': round(fraud_probability_score, 2),
            'investigator_comments': investigator_comments,
            'reported_date': reported_date.strftime('%Y-%m-%d %H:%M:%S'),
            'resolved_date': resolved_date.strftime('%Y-%m-%d %H:%M:%S') if resolved_date else None,
            'financial_impact': round(financial_impact, 2),
            'recovery_amount': round(recovery_amount, 2),
            'recovery_status': recovery_status,
            'recovery_method': recovery_method,
            'case_priority': case_priority
        }

        # Store transaction data for later linking
        fraud_case['transaction_data'] = transaction
        fraud_cases.append(fraud_case)

    return fraud_cases

# Insert data into MySQL database
def insert_data(connection, customers, merchants, transactions, fraud_cases):
    if not connection:
        print("No database connection")
        return

    cursor = connection.cursor()

    try:
        # Insert customers
        print("Inserting customers...")
        customer_query = """
        INSERT INTO Customers (
            first_name, last_name, email, phone_number, date_of_birth, gender,
            country, city, zip_code, account_open_date, account_status, annual_income,
            credit_score, risk_level, employment_status, customer_segment, linked_accounts
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        customer_values = [(
            customer['first_name'], customer['last_name'], customer['email'],
            customer['phone_number'], customer['date_of_birth'], customer['gender'],
            customer['country'], customer['city'], customer['zip_code'],
            customer['account_open_date'], customer['account_status'], customer['annual_income'],
            customer['credit_score'], customer['risk_level'], customer['employment_status'],
            customer['customer_segment'], customer['linked_accounts']
        ) for customer in customers]
        cursor.executemany(customer_query, customer_values)

        # Insert merchants
        print("Inserting merchants...")
        merchant_query = """
        INSERT INTO Merchants (
            merchant_name, merchant_category, country, city, zip_code,
            merchant_risk_score, fraudulent_flag, transaction_volume
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        merchant_values = [(
            merchant['merchant_name'], merchant['merchant_category'],
            merchant['country'], merchant['city'], merchant['zip_code'],
            merchant['merchant_risk_score'], merchant['fraudulent_flag'],
            merchant['transaction_volume']
        ) for merchant in merchants]
        cursor.executemany(merchant_query, merchant_values)

        # Fetch the actual IDs assigned by MySQL
        cursor.execute("SELECT customer_id FROM Customers")
        customer_ids = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT merchant_id FROM Merchants")
        merchant_ids = [row[0] for row in cursor.fetchall()]

        # Generate transactions with actual IDs
        print("Generating transactions with actual IDs...")
        transactions = generate_transactions(len(transactions), customer_ids, merchant_ids)

        # Insert transactions
        print("Inserting transactions...")
        transaction_query = """
        INSERT INTO Transactions (
            customer_id, merchant_id, transaction_date, transaction_amount,
            currency, transaction_type, device_used, location_lat, location_long,
            is_fraud, transaction_status, masked_card_number, card_expiry_date,
            ip_address, authentication_method, previous_transaction_time,
            time_since_last_transaction, unusual_timing_flag, distance_from_home
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        transaction_values = [(
            transaction['customer_id'], transaction['merchant_id'],
            transaction['transaction_date'], transaction['transaction_amount'],
            transaction['currency'], transaction['transaction_type'],
            transaction['device_used'], transaction['location_lat'],
            transaction['location_long'], transaction['is_fraud'],
            transaction['transaction_status'], transaction['masked_card_number'],
            transaction['card_expiry_date'], transaction['ip_address'],
            transaction['authentication_method'], transaction['previous_transaction_time'],
            transaction['time_since_last_transaction'], transaction['unusual_timing_flag'],
            transaction['distance_from_home']
        ) for transaction in transactions]
        cursor.executemany(transaction_query, transaction_values)

        # Fetch transaction IDs for fraud cases
        cursor.execute("SELECT transaction_id FROM Transactions")
        transaction_ids = [row[0] for row in cursor.fetchall()]

        # Insert fraud cases
        print("Inserting fraud cases...")
        fraud_query = """
        INSERT INTO FraudCases (
            transaction_id, fraud_reason, reported_by, resolution_status,
            fraud_probability_score, investigator_comments, reported_date,
            resolved_date, financial_impact, recovery_amount, recovery_status,
            recovery_method, case_priority
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        fraud_values = [(
            transaction_ids[i],  # Use the actual transaction_id
            fraud['fraud_reason'], fraud['reported_by'], fraud['resolution_status'],
            fraud['fraud_probability_score'], fraud['investigator_comments'],
            fraud['reported_date'], fraud['resolved_date'], fraud['financial_impact'],
            fraud['recovery_amount'], fraud['recovery_status'], fraud['recovery_method'],
            fraud['case_priority']
        ) for i, fraud in enumerate(fraud_cases)]
        cursor.executemany(fraud_query, fraud_values)

        connection.commit()
        print("All data inserted successfully!")

    except mysql.connector.Error as error:
        print(f"Error during data insertion: {error}")
        connection.rollback()
    finally:
        cursor.close()



# Main function to generate and insert data
def main():
    # Set the number of records to generate
    num_customers = 10000
    num_merchants = 2000
    num_transactions = 100000  # Adjust based on your system's capacity

    # Generate data
    start_time = time.time()

    customers = generate_customers(num_customers)
    merchants = generate_merchants(num_merchants)

    # Extract IDs (these would be assigned by the database, but we'll simulate them)
    customer_ids = list(range(1, num_customers + 1))
    merchant_ids = list(range(1, num_merchants + 1))

    transactions = generate_transactions(num_transactions, customer_ids, merchant_ids)
    fraud_cases = generate_fraud_cases(transactions)

    end_time = time.time()
    print(f"Data generation completed in {end_time - start_time:.2f} seconds")

    # Connect to database and insert data
    connection = connect_to_db()
    if connection:
        try:
            insert_data(connection, customers, merchants, transactions, fraud_cases)
        finally:
            connection.close()

    print("Database population completed!")

if __name__ == "__main__":
    main()