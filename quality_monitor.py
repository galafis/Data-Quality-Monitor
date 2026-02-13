#!/usr/bin/env python3
"""
Data Quality Monitor
Advanced data quality monitoring and validation system with automated checks and reporting.
"""

import pandas as pd
import sqlite3
import json
import os
from datetime import datetime, timedelta
from flask import Flask, render_template_string, jsonify, request
import random
import re

app = Flask(__name__)

class DataQualityMonitor:
    """Data quality monitoring and validation system."""
    
    def __init__(self, db_path="quality_monitor.db"):
        self.db_path = db_path
        self.init_database()
        self.load_sample_data()
    
    def init_database(self):
        """Initialize the quality monitoring database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Sample datasets for monitoring
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT,
                phone TEXT,
                age INTEGER,
                country TEXT,
                created_date DATE
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT,
                category TEXT,
                price DECIMAL(10,2),
                stock INTEGER,
                supplier_id INTEGER
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                product_id INTEGER,
                quantity INTEGER,
                order_date DATE,
                total_amount DECIMAL(10,2)
            )
        """)
        
        # Quality monitoring tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS quality_rules (
                rule_id INTEGER PRIMARY KEY,
                table_name TEXT,
                column_name TEXT,
                rule_type TEXT,
                rule_config TEXT,
                threshold_value REAL,
                is_active BOOLEAN DEFAULT 1,
                created_date DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS quality_results (
                result_id INTEGER PRIMARY KEY,
                rule_id INTEGER,
                table_name TEXT,
                column_name TEXT,
                check_date DATETIME,
                metric_value REAL,
                threshold_value REAL,
                status TEXT,
                details TEXT,
                FOREIGN KEY (rule_id) REFERENCES quality_rules(rule_id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS data_profiling (
                profile_id INTEGER PRIMARY KEY,
                table_name TEXT,
                column_name TEXT,
                data_type TEXT,
                total_count INTEGER,
                null_count INTEGER,
                unique_count INTEGER,
                min_value TEXT,
                max_value TEXT,
                avg_value REAL,
                std_dev REAL,
                profile_date DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def load_sample_data(self):
        """Load sample data for monitoring."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM customers")
        if cursor.fetchone()[0] > 0:
            conn.close()
            return
        
        # Sample customers with some quality issues
        customers = []
        for i in range(100):
            name = random.choice(['John Smith', 'Maria Garcia', 'Li Wei', 'Ahmed Hassan', 'Sarah Johnson', 
                                'Anna Mueller', 'Carlos Silva', 'Yuki Tanaka', '', None])  # Some null names
            
            # Generate email with some invalid formats
            if name and name != '':
                email_base = name.lower().replace(' ', '.')
                if random.random() < 0.1:  # 10% invalid emails
                    email = email_base + '@invalid'
                elif random.random() < 0.05:  # 5% null emails
                    email = None
                else:
                    email = email_base + '@email.com'
            else:
                email = None
            
            # Phone with some invalid formats
            if random.random() < 0.1:  # 10% invalid phones
                phone = '123-invalid'
            elif random.random() < 0.05:  # 5% null phones
                phone = None
            else:
                phone = f"+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
            
            # Age with some outliers
            if random.random() < 0.05:  # 5% invalid ages
                age = random.choice([0, -5, 150, 200])
            else:
                age = random.randint(18, 80)
            
            country = random.choice(['USA', 'Spain', 'China', 'Egypt', 'Canada', 'Germany', 'Brazil', 'Japan'])
            created_date = (datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d')
            
            customers.append((i+1, name, email, phone, age, country, created_date))
        
        cursor.executemany("""
            INSERT INTO customers (id, name, email, phone, age, country, created_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, customers)
        
        # Sample products with quality issues
        products = []
        categories = ['Electronics', 'Clothing', 'Books', 'Home', 'Sports']
        
        for i in range(50):
            name = f"Product {i+1}" if random.random() > 0.05 else None  # 5% null names
            category = random.choice(categories) if random.random() > 0.03 else None  # 3% null categories
            
            # Price with some negative values
            if random.random() < 0.05:  # 5% invalid prices
                price = random.choice([-10.99, 0, -100])
            else:
                price = round(random.uniform(10, 1000), 2)
            
            stock = random.randint(-5, 100) if random.random() < 0.1 else random.randint(0, 100)  # 10% negative stock
            supplier_id = random.randint(1, 10) if random.random() > 0.05 else None  # 5% null supplier
            
            products.append((i+1, name, category, price, stock, supplier_id))
        
        cursor.executemany("""
            INSERT INTO products (id, name, category, price, stock, supplier_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, products)
        
        # Sample orders
        orders = []
        for i in range(200):
            customer_id = random.randint(1, 100)
            product_id = random.randint(1, 50)
            quantity = random.randint(1, 5) if random.random() > 0.05 else 0  # 5% zero quantity
            order_date = (datetime.now() - timedelta(days=random.randint(1, 90))).strftime('%Y-%m-%d')
            
            # Get product price for total calculation
            cursor.execute("SELECT price FROM products WHERE id = ?", (product_id,))
            result = cursor.fetchone()
            price = result[0] if result and result[0] else 0
            
            total_amount = price * quantity if random.random() > 0.05 else 0  # 5% incorrect totals
            
            orders.append((i+1, customer_id, product_id, quantity, order_date, total_amount))
        
        cursor.executemany("""
            INSERT INTO orders (id, customer_id, product_id, quantity, order_date, total_amount)
            VALUES (?, ?, ?, ?, ?, ?)
        """, orders)
        
        # Initialize quality rules
        self.setup_quality_rules()
        
        conn.commit()
        conn.close()
    
    def setup_quality_rules(self):
        """Setup default quality rules."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        rules = [
            # Null checks
            ('customers', 'name', 'null_check', '{}', 5.0),
            ('customers', 'email', 'null_check', '{}', 5.0),
            ('products', 'name', 'null_check', '{}', 2.0),
            ('products', 'category', 'null_check', '{}', 3.0),
            
            # Format checks
            ('customers', 'email', 'format_check', '{"pattern": "^[\\w\\.-]+@[\\w\\.-]+\\.[a-zA-Z]{2,}$"}', 10.0),
            ('customers', 'phone', 'format_check', '{"pattern": "^\\+?[1-9]\\d{1,14}$"}', 15.0),
            
            # Range checks
            ('customers', 'age', 'range_check', '{"min": 0, "max": 120}', 5.0),
            ('products', 'price', 'range_check', '{"min": 0, "max": 10000}', 5.0),
            ('products', 'stock', 'range_check', '{"min": 0, "max": 1000}', 10.0),
            ('orders', 'quantity', 'range_check', '{"min": 1, "max": 100}', 5.0),
            
            # Uniqueness checks
            ('customers', 'email', 'uniqueness_check', '{}', 1.0),
            
            # Referential integrity
            ('orders', 'customer_id', 'foreign_key_check', '{"reference_table": "customers", "reference_column": "id"}', 0.0),
            ('orders', 'product_id', 'foreign_key_check', '{"reference_table": "products", "reference_column": "id"}', 0.0),
        ]
        
        cursor.executemany("""
            INSERT INTO quality_rules (table_name, column_name, rule_type, rule_config, threshold_value)
            VALUES (?, ?, ?, ?, ?)
        """, rules)
        
        conn.commit()
        conn.close()
    
    def _validate_table_name(self, table_name):
        """Validate that table_name exists in the database to mitigate SQL injection."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        valid_tables = {row[0] for row in cursor.fetchall()}
        conn.close()
        if table_name not in valid_tables:
            raise ValueError(f"Invalid table name: {table_name}")
    
    def run_quality_checks(self):
        """Run all active quality checks."""
        conn = sqlite3.connect(self.db_path)
        try:
            cursor = conn.cursor()
            
            # Get active rules
            cursor.execute("""
                SELECT rule_id, table_name, column_name, rule_type, rule_config, threshold_value
                FROM quality_rules
                WHERE is_active = 1
            """)
            
            rules = cursor.fetchall()
            results = []
            
            for rule in rules:
                rule_id, table_name, column_name, rule_type, rule_config, threshold_value = rule
                config = json.loads(rule_config) if rule_config else {}
                
                try:
                    if rule_type == 'null_check':
                        result = self._check_nulls(table_name, column_name, threshold_value)
                    elif rule_type == 'format_check':
                        result = self._check_format(table_name, column_name, config.get('pattern'), threshold_value)
                    elif rule_type == 'range_check':
                        result = self._check_range(table_name, column_name, config.get('min'), config.get('max'), threshold_value)
                    elif rule_type == 'uniqueness_check':
                        result = self._check_uniqueness(table_name, column_name, threshold_value)
                    elif rule_type == 'foreign_key_check':
                        result = self._check_foreign_key(table_name, column_name, config.get('reference_table'), config.get('reference_column'), threshold_value)
                    else:
                        continue
                    
                    # Store result
                    cursor.execute("""
                        INSERT INTO quality_results (rule_id, table_name, column_name, check_date, metric_value, threshold_value, status, details)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (rule_id, table_name, column_name, datetime.now(), result['metric_value'], threshold_value, result['status'], result['details']))
                    
                    results.append({
                        'rule_id': rule_id,
                        'table_name': table_name,
                        'column_name': column_name,
                        'rule_type': rule_type,
                        'metric_value': result['metric_value'],
                        'threshold_value': threshold_value,
                        'status': result['status'],
                        'details': result['details']
                    })
                    
                except Exception as e:
                    cursor.execute("""
                        INSERT INTO quality_results (rule_id, table_name, column_name, check_date, metric_value, threshold_value, status, details)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (rule_id, table_name, column_name, datetime.now(), 0, threshold_value, 'ERROR', str(e)))
            
            conn.commit()
        finally:
            conn.close()
        
        return results
    
    def _check_nulls(self, table_name, column_name, threshold):
        """Check null percentage."""
        self._validate_table_name(table_name)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        total_count = cursor.fetchone()[0]
        
        cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE {column_name} IS NULL OR {column_name} = ''")
        null_count = cursor.fetchone()[0]
        
        conn.close()
        
        null_percentage = (null_count / total_count * 100) if total_count > 0 else 0
        status = 'PASS' if null_percentage <= threshold else 'FAIL'
        
        return {
            'metric_value': null_percentage,
            'status': status,
            'details': f'{null_count}/{total_count} null values ({null_percentage:.2f}%)'
        }
    
    def _check_format(self, table_name, column_name, pattern, threshold):
        """Check format compliance."""
        self._validate_table_name(table_name)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT {column_name} FROM {table_name} WHERE {column_name} IS NOT NULL AND {column_name} != ''")
        values = cursor.fetchall()
        
        conn.close()
        
        if not values:
            return {'metric_value': 0, 'status': 'PASS', 'details': 'No values to check'}
        
        invalid_count = 0
        for value in values:
            if not re.match(pattern, str(value[0])):
                invalid_count += 1
        
        invalid_percentage = (invalid_count / len(values) * 100)
        status = 'PASS' if invalid_percentage <= threshold else 'FAIL'
        
        return {
            'metric_value': invalid_percentage,
            'status': status,
            'details': f'{invalid_count}/{len(values)} invalid format ({invalid_percentage:.2f}%)'
        }
    
    def _check_range(self, table_name, column_name, min_val, max_val, threshold):
        """Check value range compliance."""
        self._validate_table_name(table_name)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE {column_name} IS NOT NULL")
        total_count = cursor.fetchone()[0]
        
        if min_val is not None and max_val is not None:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE {column_name} < ? OR {column_name} > ?", (min_val, max_val))
        elif min_val is not None:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE {column_name} < ?", (min_val,))
        elif max_val is not None:
            cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE {column_name} > ?", (max_val,))
        else:
            conn.close()
            return {'metric_value': 0, 'status': 'PASS', 'details': 'No range specified'}
        
        out_of_range_count = cursor.fetchone()[0]
        conn.close()
        
        out_of_range_percentage = (out_of_range_count / total_count * 100) if total_count > 0 else 0
        status = 'PASS' if out_of_range_percentage <= threshold else 'FAIL'
        
        return {
            'metric_value': out_of_range_percentage,
            'status': status,
            'details': f'{out_of_range_count}/{total_count} out of range ({out_of_range_percentage:.2f}%)'
        }
    
    def _check_uniqueness(self, table_name, column_name, threshold):
        """Check uniqueness constraint."""
        self._validate_table_name(table_name)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE {column_name} IS NOT NULL")
        total_count = cursor.fetchone()[0]
        
        cursor.execute(f"SELECT COUNT(DISTINCT {column_name}) FROM {table_name} WHERE {column_name} IS NOT NULL")
        unique_count = cursor.fetchone()[0]
        
        conn.close()
        
        duplicate_count = total_count - unique_count
        duplicate_percentage = (duplicate_count / total_count * 100) if total_count > 0 else 0
        status = 'PASS' if duplicate_percentage <= threshold else 'FAIL'
        
        return {
            'metric_value': duplicate_percentage,
            'status': status,
            'details': f'{duplicate_count} duplicates ({duplicate_percentage:.2f}%)'
        }
    
    def _check_foreign_key(self, table_name, column_name, ref_table, ref_column, threshold):
        """Check foreign key integrity."""
        self._validate_table_name(table_name)
        self._validate_table_name(ref_table)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(f"""
            SELECT COUNT(*) FROM {table_name} t
            LEFT JOIN {ref_table} r ON t.{column_name} = r.{ref_column}
            WHERE t.{column_name} IS NOT NULL AND r.{ref_column} IS NULL
        """)
        orphan_count = cursor.fetchone()[0]
        
        cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE {column_name} IS NOT NULL")
        total_count = cursor.fetchone()[0]
        
        conn.close()
        
        orphan_percentage = (orphan_count / total_count * 100) if total_count > 0 else 0
        status = 'PASS' if orphan_percentage <= threshold else 'FAIL'
        
        return {
            'metric_value': orphan_percentage,
            'status': status,
            'details': f'{orphan_count} orphan records ({orphan_percentage:.2f}%)'
        }
    
    def get_quality_summary(self):
        """Get quality summary and trends."""
        conn = sqlite3.connect(self.db_path)
        
        # Latest results summary
        query = """
            SELECT 
                table_name,
                COUNT(*) as total_checks,
                SUM(CASE WHEN status = 'PASS' THEN 1 ELSE 0 END) as passed_checks,
                SUM(CASE WHEN status = 'FAIL' THEN 1 ELSE 0 END) as failed_checks,
                AVG(metric_value) as avg_metric_value
            FROM quality_results
            WHERE check_date >= datetime('now', '-1 day')
            GROUP BY table_name
        """
        
        summary = pd.read_sql_query(query, conn).to_dict('records')
        
        # Quality trends over time
        query = """
            SELECT 
                DATE(check_date) as check_date,
                COUNT(*) as total_checks,
                SUM(CASE WHEN status = 'PASS' THEN 1 ELSE 0 END) as passed_checks,
                ROUND(AVG(metric_value), 2) as avg_metric_value
            FROM quality_results
            WHERE check_date >= datetime('now', '-30 days')
            GROUP BY DATE(check_date)
            ORDER BY check_date
        """
        
        trends = pd.read_sql_query(query, conn).to_dict('records')
        
        # Recent failed checks
        query = """
            SELECT 
                table_name,
                column_name,
                metric_value,
                threshold_value,
                details,
                check_date
            FROM quality_results
            WHERE status = 'FAIL'
            ORDER BY check_date DESC
            LIMIT 10
        """
        
        failed_checks = pd.read_sql_query(query, conn).to_dict('records')
        
        conn.close()
        
        return {
            'summary': summary,
            'trends': trends,
            'failed_checks': failed_checks
        }
    
    def profile_data(self, table_name):
        """Profile data for a specific table."""
        self._validate_table_name(table_name)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get table columns
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()
        
        profiles = []
        
        for column in columns:
            column_name = column[1]
            data_type = column[2]
            
            # Basic statistics
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            total_count = cursor.fetchone()[0]
            
            cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE {column_name} IS NULL OR {column_name} = ''")
            null_count = cursor.fetchone()[0]
            
            cursor.execute(f"SELECT COUNT(DISTINCT {column_name}) FROM {table_name} WHERE {column_name} IS NOT NULL")
            unique_count = cursor.fetchone()[0]
            
            # Type-specific statistics
            min_value = max_value = avg_value = std_dev = None
            
            if data_type in ['INTEGER', 'REAL', 'DECIMAL']:
                cursor.execute(f"SELECT MIN({column_name}), MAX({column_name}), AVG({column_name}) FROM {table_name} WHERE {column_name} IS NOT NULL")
                result = cursor.fetchone()
                if result:
                    min_value, max_value, avg_value = result
                
                # Calculate standard deviation
                if avg_value is not None:
                    cursor.execute(f"SELECT AVG(({column_name} - ?)* ({column_name} - ?)) FROM {table_name} WHERE {column_name} IS NOT NULL", (avg_value, avg_value))
                    variance = cursor.fetchone()[0]
                    std_dev = variance ** 0.5 if variance else 0
            
            elif data_type == 'TEXT':
                cursor.execute(f"SELECT MIN(LENGTH({column_name})), MAX(LENGTH({column_name})), AVG(LENGTH({column_name})) FROM {table_name} WHERE {column_name} IS NOT NULL")
                result = cursor.fetchone()
                if result:
                    min_value, max_value, avg_value = result
            
            profiles.append({
                'column_name': column_name,
                'data_type': data_type,
                'total_count': total_count,
                'null_count': null_count,
                'unique_count': unique_count,
                'min_value': min_value,
                'max_value': max_value,
                'avg_value': avg_value,
                'std_dev': std_dev,
                'null_percentage': (null_count / total_count * 100) if total_count > 0 else 0,
                'unique_percentage': (unique_count / total_count * 100) if total_count > 0 else 0
            })
        
        conn.close()
        return profiles

monitor = None

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data Quality Monitor</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }
        
        .header {
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            text-align: center;
        }
        
        .nav-tabs {
            display: flex;
            background: white;
            border-radius: 15px;
            padding: 5px;
            margin-bottom: 20px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        
        .nav-tab {
            flex: 1;
            padding: 15px;
            text-align: center;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: 600;
        }
        
        .nav-tab.active {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .tab-content {
            display: none;
        }
        
        .tab-content.active {
            display: block;
        }
        
        .card {
            background: white;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 15px;
            padding: 25px;
            text-align: center;
        }
        
        .metric-value {
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 10px;
        }
        
        .metric-label {
            font-size: 1rem;
            opacity: 0.9;
        }
        
        .data-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        
        .data-table th,
        .data-table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e0e0e0;
        }
        
        .data-table th {
            background: #f8f9fa;
            font-weight: 600;
        }
        
        .status-pass {
            color: #27ae60;
            font-weight: bold;
        }
        
        .status-fail {
            color: #e74c3c;
            font-weight: bold;
        }
        
        .status-error {
            color: #f39c12;
            font-weight: bold;
        }
        
        .btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-weight: 600;
            margin: 10px 5px;
        }
        
        .btn:hover {
            opacity: 0.9;
        }
        
        .chart-container {
            height: 300px;
            margin: 20px 0;
        }
        
        .profile-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }
        
        .profile-card {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
        }
        
        .profile-stat {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #e0e0e0;
        }
        
        .profile-stat:last-child {
            border-bottom: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔍 Data Quality Monitor</h1>
            <p>Advanced data quality monitoring and validation system</p>
        </div>
        
        <div class="nav-tabs">
            <div class="nav-tab active" onclick="showTab('dashboard')">📊 Dashboard</div>
            <div class="nav-tab" onclick="showTab('checks')">✅ Quality Checks</div>
            <div class="nav-tab" onclick="showTab('profiling')">📈 Data Profiling</div>
        </div>
        
        <div id="dashboard" class="tab-content active">
            <div class="metrics-grid" id="metricsGrid">
                <!-- Metrics will be populated here -->
            </div>
            
            <div class="card">
                <h3>📈 Quality Trends</h3>
                <div class="chart-container">
                    <canvas id="trendsChart"></canvas>
                </div>
            </div>
            
            <div class="card">
                <h3>⚠️ Recent Failed Checks</h3>
                <table class="data-table" id="failedChecksTable">
                    <thead>
                        <tr>
                            <th>Table</th>
                            <th>Column</th>
                            <th>Metric Value</th>
                            <th>Threshold</th>
                            <th>Details</th>
                            <th>Check Date</th>
                        </tr>
                    </thead>
                    <tbody id="failedChecksBody">
                        <!-- Failed checks will be populated here -->
                    </tbody>
                </table>
            </div>
        </div>
        
        <div id="checks" class="tab-content">
            <div class="card">
                <h3>✅ Quality Check Results</h3>
                <button onclick="runQualityChecks()" class="btn">🔄 Run All Checks</button>
                <table class="data-table" id="checksTable">
                    <thead>
                        <tr>
                            <th>Table</th>
                            <th>Column</th>
                            <th>Rule Type</th>
                            <th>Metric Value</th>
                            <th>Threshold</th>
                            <th>Status</th>
                            <th>Details</th>
                        </tr>
                    </thead>
                    <tbody id="checksBody">
                        <!-- Check results will be populated here -->
                    </tbody>
                </table>
            </div>
        </div>
        
        <div id="profiling" class="tab-content">
            <div class="card">
                <h3>📈 Data Profiling</h3>
                <button onclick="profileTable('customers')" class="btn">👥 Profile Customers</button>
                <button onclick="profileTable('products')" class="btn">📦 Profile Products</button>
                <button onclick="profileTable('orders')" class="btn">🛒 Profile Orders</button>
                
                <div id="profilingResults" class="profile-grid">
                    <!-- Profiling results will be populated here -->
                </div>
            </div>
        </div>
    </div>

    <script>
        let dashboardData = null;
        
        function showTab(tabName) {
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Remove active class from all nav tabs
            document.querySelectorAll('.nav-tab').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Show selected tab
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
            
            // Load data based on tab
            if (tabName === 'dashboard' && !dashboardData) {
                loadDashboard();
            }
        }
        
        async function loadDashboard() {
            try {
                const response = await fetch('/quality-summary');
                dashboardData = await response.json();
                
                displayMetrics(dashboardData.summary);
                createTrendsChart(dashboardData.trends);
                displayFailedChecks(dashboardData.failed_checks);
                
            } catch (error) {
                console.error('Error loading dashboard:', error);
            }
        }
        
        function displayMetrics(summary) {
            const metricsGrid = document.getElementById('metricsGrid');
            
            let totalChecks = 0;
            let totalPassed = 0;
            let totalFailed = 0;
            
            summary.forEach(table => {
                totalChecks += table.total_checks;
                totalPassed += table.passed_checks;
                totalFailed += table.failed_checks;
            });
            
            const passRate = totalChecks > 0 ? (totalPassed / totalChecks * 100).toFixed(1) : 0;
            
            metricsGrid.innerHTML = `
                <div class="metric-card">
                    <div class="metric-value">${totalChecks}</div>
                    <div class="metric-label">Total Checks</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">${totalPassed}</div>
                    <div class="metric-label">Passed Checks</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">${totalFailed}</div>
                    <div class="metric-label">Failed Checks</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">${passRate}%</div>
                    <div class="metric-label">Pass Rate</div>
                </div>
            `;
        }
        
        function createTrendsChart(trends) {
            const ctx = document.getElementById('trendsChart').getContext('2d');
            
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: trends.map(d => d.check_date),
                    datasets: [{
                        label: 'Total Checks',
                        data: trends.map(d => d.total_checks),
                        borderColor: '#667eea',
                        backgroundColor: '#667eea20',
                        tension: 0.4
                    }, {
                        label: 'Passed Checks',
                        data: trends.map(d => d.passed_checks),
                        borderColor: '#27ae60',
                        backgroundColor: '#27ae6020',
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }
        
        function displayFailedChecks(failedChecks) {
            const tbody = document.getElementById('failedChecksBody');
            
            tbody.innerHTML = failedChecks.map(check => `
                <tr>
                    <td>${check.table_name}</td>
                    <td>${check.column_name}</td>
                    <td>${check.metric_value}</td>
                    <td>${check.threshold_value}</td>
                    <td>${check.details}</td>
                    <td>${new Date(check.check_date).toLocaleString()}</td>
                </tr>
            `).join('');
        }
        
        async function runQualityChecks() {
            try {
                const response = await fetch('/run-checks', { method: 'POST' });
                const results = await response.json();
                
                displayCheckResults(results);
                
                // Refresh dashboard
                loadDashboard();
                
            } catch (error) {
                console.error('Error running checks:', error);
            }
        }
        
        function displayCheckResults(results) {
            const tbody = document.getElementById('checksBody');
            
            tbody.innerHTML = results.map(result => `
                <tr>
                    <td>${result.table_name}</td>
                    <td>${result.column_name}</td>
                    <td>${result.rule_type}</td>
                    <td>${result.metric_value.toFixed(2)}</td>
                    <td>${result.threshold_value}</td>
                    <td class="status-${result.status.toLowerCase()}">${result.status}</td>
                    <td>${result.details}</td>
                </tr>
            `).join('');
        }
        
        async function profileTable(tableName) {
            try {
                const response = await fetch(`/profile/${tableName}`);
                const profiles = await response.json();
                
                displayProfiles(profiles, tableName);
                
            } catch (error) {
                console.error('Error profiling table:', error);
            }
        }
        
        function displayProfiles(profiles, tableName) {
            const container = document.getElementById('profilingResults');
            
            container.innerHTML = `<h4>📊 ${tableName.toUpperCase()} Profile</h4>` + 
                profiles.map(profile => `
                    <div class="profile-card">
                        <h5>${profile.column_name} (${profile.data_type})</h5>
                        <div class="profile-stat">
                            <span>Total Count:</span>
                            <span>${profile.total_count}</span>
                        </div>
                        <div class="profile-stat">
                            <span>Null Count:</span>
                            <span>${profile.null_count} (${profile.null_percentage.toFixed(1)}%)</span>
                        </div>
                        <div class="profile-stat">
                            <span>Unique Count:</span>
                            <span>${profile.unique_count} (${profile.unique_percentage.toFixed(1)}%)</span>
                        </div>
                        ${profile.min_value !== null ? `
                            <div class="profile-stat">
                                <span>Min Value:</span>
                                <span>${profile.min_value}</span>
                            </div>
                        ` : ''}
                        ${profile.max_value !== null ? `
                            <div class="profile-stat">
                                <span>Max Value:</span>
                                <span>${profile.max_value}</span>
                            </div>
                        ` : ''}
                        ${profile.avg_value !== null ? `
                            <div class="profile-stat">
                                <span>Average:</span>
                                <span>${profile.avg_value.toFixed(2)}</span>
                            </div>
                        ` : ''}
                        ${profile.std_dev !== null ? `
                            <div class="profile-stat">
                                <span>Std Deviation:</span>
                                <span>${profile.std_dev.toFixed(2)}</span>
                            </div>
                        ` : ''}
                    </div>
                `).join('');
        }
        
        // Load dashboard on page load
        document.addEventListener('DOMContentLoaded', function() {
            loadDashboard();
        });
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """Main dashboard page."""
    return render_template_string(HTML_TEMPLATE)

@app.route('/quality-summary')
def get_quality_summary():
    """Get quality summary and trends."""
    try:
        return jsonify(monitor.get_quality_summary())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/run-checks', methods=['POST'])
def run_checks():
    """Run all quality checks."""
    try:
        results = monitor.run_quality_checks()
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/profile/<table_name>')
def profile_table(table_name):
    """Profile a specific table."""
    try:
        profiles = monitor.profile_data(table_name)
        return jsonify(profiles)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def main():
    """Main execution function."""
    global monitor
    monitor = DataQualityMonitor()
    
    print("Data Quality Monitor")
    print("=" * 30)
    
    print("Initializing quality monitoring system...")
    print("Loading sample data with quality issues...")
    print("Setting up quality rules...")
    print("Starting web server...")
    print("Open http://localhost:5000 in your browser")
    
    app.run(debug=False, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    main()

