"""
============================================
DBMS Project: Startup Funding System
Student 3: Application & User Module
============================================
Flask application with database connectivity
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from mysql.connector import Error
import bcrypt
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'  # Change this!
app.permanent_session_lifetime = timedelta(hours=24)

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',  # Change this!
    'database': 'funding_system'
}

# ============================================
# Database Connection Helper
# ============================================

def get_db_connection():
    """Create and return database connection"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Database connection error: {e}")
        return None

# ============================================
# Authentication Functions
# ============================================

def hash_password(password):
    """Hash password using bcrypt"""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(password, hashed):
    """Verify password against hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

# ============================================
# Routes: Home & Landing
# ============================================

@app.route('/')
def index():
    """Landing page"""
    return render_template('index.html')

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

# ============================================
# Routes: Startup Registration & Login
# ============================================

@app.route('/startup/register', methods=['GET', 'POST'])
def startup_register():
    """Startup registration"""
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        domain_id = request.form.get('domain_id')
        funding_required = request.form.get('funding_required')
        description = request.form.get('description')
        founded_date = request.form.get('founded_date')
        location = request.form.get('location')
        website = request.form.get('website', '')
        
        # Hash password
        password_hash = hash_password(password)
        
        # Insert into database
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                query = """
                    INSERT INTO Startups 
                    (name, email, password_hash, domain_id, funding_required, 
                     description, founded_date, location, website)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (name, email, password_hash, domain_id, 
                                      funding_required, description, founded_date, 
                                      location, website))
                conn.commit()
                
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('startup_login'))
            
            except Error as e:
                flash(f'Registration failed: {str(e)}', 'error')
            finally:
                cursor.close()
                conn.close()
    
    # GET request - show form with domains
    conn = get_db_connection()
    domains = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Domains")
        domains = cursor.fetchall()
        cursor.close()
        conn.close()
    
    return render_template('startup_register.html', domains=domains)

@app.route('/startup/login', methods=['GET', 'POST'])
def startup_login():
    """Startup login"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("""
                    SELECT startup_id, name, email, password_hash 
                    FROM Startups WHERE email = %s
                """, (email,))
                
                startup = cursor.fetchone()
                
                if startup and verify_password(password, startup['password_hash']):
                    # Set session
                    session.permanent = True
                    session['user_type'] = 'startup'
                    session['user_id'] = startup['startup_id']
                    session['user_name'] = startup['name']
                    
                    flash(f'Welcome back, {startup["name"]}!', 'success')
                    return redirect(url_for('startup_dashboard'))
                else:
                    flash('Invalid email or password', 'error')
            
            except Error as e:
                flash(f'Login failed: {str(e)}', 'error')
            finally:
                cursor.close()
                conn.close()
    
    return render_template('startup_login.html')

# ============================================
# Routes: Startup Dashboard
# ============================================

@app.route('/startup/dashboard')
def startup_dashboard():
    """Startup dashboard - shows matched investors"""
    if 'user_type' not in session or session['user_type'] != 'startup':
        flash('Please login first', 'error')
        return redirect(url_for('startup_login'))
    
    startup_id = session['user_id']
    
    conn = get_db_connection()
    if not conn:
        flash('Database connection error', 'error')
        return redirect(url_for('index'))
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Get startup details
        cursor.execute("""
            SELECT s.*, d.domain_name,
                   COALESCE(SUM(f.amount), 0) AS total_funding_received
            FROM Startups s
            JOIN Domains d ON s.domain_id = d.domain_id
            LEFT JOIN Funding f ON s.startup_id = f.startup_id
            WHERE s.startup_id = %s
            GROUP BY s.startup_id
        """, (startup_id,))
        startup = cursor.fetchone()
        
        # Get matched investors (MATCHMAKING ALGORITHM)
        cursor.execute("""
            SELECT 
                i.investor_id,
                i.name,
                i.investment_min,
                i.investment_max,
                i.preferred_domains,
                i.location,
                i.portfolio_size,
                CASE 
                    WHEN FIND_IN_SET(%s, i.preferred_domains) > 0 THEN 100
                    ELSE 50
                END AS match_score,
                CASE 
                    WHEN FIND_IN_SET(%s, i.preferred_domains) > 0 THEN 'Perfect domain match'
                    ELSE 'Investment range compatible'
                END AS match_reason
            FROM Investors i
            WHERE i.investment_min <= %s 
              AND i.investment_max >= %s
            ORDER BY match_score DESC, i.portfolio_size ASC
            LIMIT 10
        """, (startup['domain_id'], startup['domain_id'], 
              startup['funding_required'], startup['funding_required']))
        
        matched_investors = cursor.fetchall()
        
        # Get funding history
        cursor.execute("""
            SELECT f.*, i.name AS investor_name
            FROM Funding f
            JOIN Investors i ON f.investor_id = i.investor_id
            WHERE f.startup_id = %s
            ORDER BY f.funding_date DESC
        """, (startup_id,))
        
        funding_history = cursor.fetchall()
        
        return render_template('startup_dashboard.html', 
                             startup=startup,
                             matched_investors=matched_investors,
                             funding_history=funding_history)
    
    except Error as e:
        flash(f'Error loading dashboard: {str(e)}', 'error')
        return redirect(url_for('index'))
    finally:
        cursor.close()
        conn.close()

# ============================================
# Routes: Investor Registration & Login
# ============================================

@app.route('/investor/register', methods=['GET', 'POST'])
def investor_register():
    """Investor registration"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        investment_min = request.form.get('investment_min')
        investment_max = request.form.get('investment_max')
        preferred_domains = request.form.get('preferred_domains')  # Comma-separated IDs
        phone = request.form.get('phone')
        location = request.form.get('location')
        
        password_hash = hash_password(password)
        
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                query = """
                    INSERT INTO Investors 
                    (name, email, password_hash, investment_min, investment_max, 
                     preferred_domains, phone, location)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (name, email, password_hash, investment_min, 
                                      investment_max, preferred_domains, phone, location))
                conn.commit()
                
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('investor_login'))
            
            except Error as e:
                flash(f'Registration failed: {str(e)}', 'error')
            finally:
                cursor.close()
                conn.close()
    
    # GET request - show form with domains
    conn = get_db_connection()
    domains = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Domains")
        domains = cursor.fetchall()
        cursor.close()
        conn.close()
    
    return render_template('investor_register.html', domains=domains)

@app.route('/investor/login', methods=['GET', 'POST'])
def investor_login():
    """Investor login"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor(dictionary=True)
                cursor.execute("""
                    SELECT investor_id, name, email, password_hash 
                    FROM Investors WHERE email = %s
                """, (email,))
                
                investor = cursor.fetchone()
                
                if investor and verify_password(password, investor['password_hash']):
                    session.permanent = True
                    session['user_type'] = 'investor'
                    session['user_id'] = investor['investor_id']
                    session['user_name'] = investor['name']
                    
                    flash(f'Welcome back, {investor["name"]}!', 'success')
                    return redirect(url_for('investor_dashboard'))
                else:
                    flash('Invalid email or password', 'error')
            
            except Error as e:
                flash(f'Login failed: {str(e)}', 'error')
            finally:
                cursor.close()
                conn.close()
    
    return render_template('investor_login.html')

# ============================================
# Routes: Investor Dashboard
# ============================================

@app.route('/investor/dashboard')
def investor_dashboard():
    """Investor dashboard - shows matched startups"""
    if 'user_type' not in session or session['user_type'] != 'investor':
        flash('Please login first', 'error')
        return redirect(url_for('investor_login'))
    
    investor_id = session['user_id']
    
    conn = get_db_connection()
    if not conn:
        flash('Database connection error', 'error')
        return redirect(url_for('index'))
    
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Get investor details
        cursor.execute("""
            SELECT i.*, 
                   COALESCE(SUM(f.amount), 0) AS total_invested,
                   COUNT(DISTINCT f.startup_id) AS startups_funded
            FROM Investors i
            LEFT JOIN Funding f ON i.investor_id = f.investor_id
            WHERE i.investor_id = %s
            GROUP BY i.investor_id
        """, (investor_id,))
        investor = cursor.fetchone()
        
        # Get matched startups
        cursor.execute("""
            SELECT 
                s.startup_id,
                s.name,
                d.domain_name,
                s.funding_required,
                s.location,
                s.description,
                s.is_funded,
                CASE 
                    WHEN FIND_IN_SET(s.domain_id, %s) > 0 THEN 100
                    ELSE 50
                END AS match_score
            FROM Startups s
            JOIN Domains d ON s.domain_id = d.domain_id
            WHERE s.funding_required BETWEEN %s AND %s
              AND s.is_funded = FALSE
            ORDER BY match_score DESC, s.founded_date DESC
            LIMIT 10
        """, (investor['preferred_domains'], investor['investment_min'], 
              investor['investment_max']))
        
        matched_startups = cursor.fetchall()
        
        # Get portfolio (funded startups)
        cursor.execute("""
            SELECT f.*, s.name AS startup_name, d.domain_name
            FROM Funding f
            JOIN Startups s ON f.startup_id = s.startup_id
            JOIN Domains d ON s.domain_id = d.domain_id
            WHERE f.investor_id = %s
            ORDER BY f.funding_date DESC
        """, (investor_id,))
        
        portfolio = cursor.fetchall()
        
        return render_template('investor_dashboard.html',
                             investor=investor,
                             matched_startups=matched_startups,
                             portfolio=portfolio)
    
    except Error as e:
        flash(f'Error loading dashboard: {str(e)}', 'error')
        return redirect(url_for('index'))
    finally:
        cursor.close()
        conn.close()

# ============================================
# Routes: Logout
# ============================================

@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

# ============================================
# Run Application
# ============================================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

