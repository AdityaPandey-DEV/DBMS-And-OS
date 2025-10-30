# 🚀 Quick Start Guide

Get both projects running in 5 minutes!

## ⚡ DBMS Project (Startup Funding System)

### Prerequisites
- MySQL Server 5.7+
- Python 3.7+

### 3-Step Setup

**Step 1**: Create Database
```bash
mysql -u root -p
CREATE DATABASE funding_system;
EXIT;
```

**Step 2**: Import Schema & Data
```bash
cd DBMS_Project
mysql -u root -p funding_system < database_schema.sql
```

**Step 3**: Configure & Run
```bash
# Edit app.py - Update password in DB_CONFIG
nano app.py  # Change 'your_password' to your MySQL password

# Install dependencies & run
pip install -r requirements.txt
python app.py
```

**Step 4**: Open Browser
```
http://localhost:5000
```

### ✅ Verify Installation

```bash
# Login to MySQL
mysql -u root -p funding_system

# Check tables
SHOW TABLES;
# Should show: Domains, Startups, Investors, Funding, Matches

# Check sample data
SELECT * FROM Startups LIMIT 3;
# Should show: AI Insights, FinFlow, MediCare AI

# Exit
EXIT;
```

### 🎬 Demo DBMS Project

1. **View Sample Data**:
   ```sql
   mysql -u root -p funding_system
   SELECT * FROM Startups;
   SELECT * FROM Investors;
   ```

2. **Test Matchmaking Query**:
   ```sql
   -- Find investors for startup ID 1
   SELECT i.name, i.investment_min, i.investment_max
   FROM Investors i
   CROSS JOIN Startups s
   WHERE s.startup_id = 1
     AND i.investment_min <= s.funding_required 
     AND i.investment_max >= s.funding_required;
   ```

3. **Generate Report**:
   ```sql
   -- Top Investors Report
   SELECT 
       i.name AS Investor,
       COUNT(f.funding_id) AS Startups_Funded,
       SUM(f.amount) AS Total_Investment
   FROM Investors i
   JOIN Funding f ON i.investor_id = f.investor_id
   GROUP BY i.investor_id
   ORDER BY Total_Investment DESC;
   ```

---

## ⚡ OS Project (Blockchain File Access Control)

### Prerequisites
- Python 3.7+ (that's it! No other dependencies!)

### 1-Step Setup

```bash
cd OS_Project
python main.py --demo
```

That's it! The demo will run automatically.

### ✅ Verify Installation

**Test Student 1 (Blockchain)**:
```bash
python blockchain.py
```
Expected output:
```
✓ Genesis block created
Block 1: User1 created file.txt
Block 2: User2 read file.txt
✓ Blockchain is VALID
--- After tampering ---
✗ Blockchain is INVALID - Tampering detected!
```

**Test Student 2 (File Manager)**:
```bash
python file_manager.py
```
Expected output:
```
✓ User registered: Admin (Admin)
✓ File created: test.txt by admin001
✓ File read: test.txt by admin001
```

**Test Student 3 (Access Control)**:
```bash
python access_control.py
```
Expected output:
```
Permission Matrix:
  Admin  → Full access
  User   → Own files + public
  Guest  → Public only (read-only)

Scenario: Guest tries to delete file
  ✗ Access denied → Logged to blockchain
```

**Test Student 4 (Audit Reports)**:
```bash
python audit_reports.py
```
Expected output:
```
FILE ACCESS REPORT: report.txt
───────────────────────────────────
3 access attempts (2 success, 1 denied)

SECURITY REPORT:
  3 unauthorized attempts detected
  • guest001: 2 violations
```

### 🎬 Demo OS Project

**Interactive Mode**:
```bash
python main.py
```

Menu options:
```
1. Login (try: admin001, user001, guest001)
2. Create File
3. Read File
4. Delete File
8. Generate Reports
9. View Blockchain
```

**Automated Demo Mode**:
```bash
python main.py --demo
```

This runs a complete demonstration:
- Creates 3 users (Admin, User, Guest)
- Performs 10+ file operations
- Shows access control in action
- Generates security reports
- Displays blockchain

---

## 🎯 Testing Each Student's Work

### DBMS Project

**Student 1 (Database)**:
```bash
mysql -u root -p funding_system
SHOW TABLES;
DESCRIBE Startups;
SHOW CREATE TABLE Funding;  # See foreign keys
```

**Student 2 (Queries)**:
```bash
mysql -u root -p funding_system
# Run queries from queries.sql
SOURCE queries.sql;
# Test stored procedure
CALL RecordFunding(1, 1, 5000000, 'Seed', 'Test');
```

**Student 3 (Application)**:
```bash
python app.py
# Open http://localhost:5000
# Test registration, login, dashboard
```

**Student 4 (Reports)**:
```bash
mysql -u root -p funding_system
# Run reports from reports.sql
SOURCE reports.sql;
```

---

### OS Project

**Student 1 (Blockchain)**:
```bash
python blockchain.py
# Shows: Block creation, hashing, validation, tampering detection
```

**Student 2 (File Manager)**:
```bash
python file_manager.py
# Shows: User management, file operations, blockchain logging
```

**Student 3 (Access Control)**:
```bash
python access_control.py
# Shows: RBAC matrix, permission checks, denied access logging
```

**Student 4 (Audit Reports)**:
```bash
python audit_reports.py
# Shows: Query functions, reports, security violations, exports
```

---

## 🐛 Troubleshooting

### DBMS Project Issues

**Issue**: `Access denied for user 'root'@'localhost'`
```bash
# Fix: Update password in app.py
nano app.py
# Change DB_CONFIG['password'] = 'your_actual_password'
```

**Issue**: `ModuleNotFoundError: No module named 'flask'`
```bash
pip install -r requirements.txt
```

**Issue**: `Table 'Startups' already exists`
```bash
# Drop and recreate
mysql -u root -p
DROP DATABASE funding_system;
CREATE DATABASE funding_system;
EXIT;
# Re-import
mysql -u root -p funding_system < database_schema.sql
```

### OS Project Issues

**Issue**: `FileNotFoundError: './files/...'`
```bash
# Solution: Directory auto-creates. Restart program.
python main.py --demo
```

**Issue**: Blockchain validation fails
```bash
# This is intentional for tampering demo!
# Restart to get clean blockchain:
python main.py --demo
```

---

## 📝 Next Steps

### For Faculty Presentation

**DBMS Project** (10 min demo):
1. Show ER diagram (Student 1)
2. Run matchmaking query (Student 2)
3. Demo live app (Student 3)
4. Generate reports (Student 4)

**OS Project** (10 min demo):
```bash
python main.py --demo
```
This automatically demonstrates all 4 modules!

### For Development/Customization

**DBMS Project**:
- Add more domains: Edit `database_schema.sql`
- Modify matchmaking: Edit queries in `queries.sql`
- Customize UI: Create HTML templates (see `app.py` routes)
- Add features: Extend `app.py`

**OS Project**:
- Add encryption: Modify `blockchain.py` to encrypt data
- Add more roles: Edit `PERMISSIONS` in `access_control.py`
- Add notifications: Extend `audit_reports.py`
- Web interface: Wrap `main.py` with Flask (like DBMS)

---

## ✅ Success Checklist

### DBMS Project Working If:
- [x] Database created with 5 tables
- [x] Sample data imported (5 startups, 5 investors)
- [x] Flask app runs on port 5000
- [x] Can login and see dashboard
- [x] Matchmaking shows investors
- [x] Reports generate data

### OS Project Working If:
- [x] `python blockchain.py` shows blockchain
- [x] `python file_manager.py` creates files
- [x] `python access_control.py` shows permission matrix
- [x] `python audit_reports.py` generates reports
- [x] `python main.py --demo` runs full demo
- [x] Blockchain detects tampering

---

## 🎓 For Students

### Preparing for Viva/Presentation

**Each student should**:
1. Read their `Student_X_Script.md` (2-3 min presentation)
2. Run their module independently
3. Understand how their code works
4. Be ready to answer 5 common questions (in script)
5. Know how their module connects to others

**Practice Demo**:
- Student 1: 2 min
- Student 2: 2 min
- Student 3: 2 min
- Student 4: 2 min
- **Total**: 8 minutes + 2 min Q&A = **10 minutes**

### Day Before Presentation

- [ ] Test both projects end-to-end
- [ ] Prepare ER diagram (DBMS) or architecture diagram (OS)
- [ ] Practice speaking parts
- [ ] Prepare backup screenshots (in case demo fails)
- [ ] Charge laptop, check internet/database access

---

**Need Help?** Check individual `README.md` files in each project folder for detailed documentation!

