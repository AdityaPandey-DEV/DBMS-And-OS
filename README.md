# 🎓 Academic Projects: DBMS & OS

Complete implementation and documentation for two academic projects with clear task divisions for 4 students each.

## 📁 Project Structure

```
├── DBMS_Project/                    # Startup Funding System
│   ├── database_schema.sql          # ✅ COMPLETE - Database schema
│   ├── queries.sql                  # ✅ COMPLETE - SQL queries
│   ├── app.py                       # ✅ COMPLETE - Flask application
│   ├── reports.sql                  # ✅ COMPLETE - Report queries
│   ├── requirements.txt             # Python dependencies
│   ├── README.md                    # Setup & testing guide
│   ├── Task_Division.md             # Module-wise responsibilities
│   ├── Student_1_Script.md          # Presentation script (Database)
│   ├── Student_2_Script.md          # Presentation script (Queries)
│   ├── Student_3_Script.md          # Presentation script (Application)
│   └── Student_4_Script.md          # Presentation script (Reports)
│
└── OS_Project/                      # Blockchain File Access Control
    ├── blockchain.py                # ✅ COMPLETE - Blockchain core
    ├── file_manager.py              # ✅ COMPLETE - File operations
    ├── access_control.py            # ✅ COMPLETE - RBAC security
    ├── audit_reports.py             # ✅ COMPLETE - Audit & reports
    ├── main.py                      # ✅ COMPLETE - Integrated app
    ├── requirements.txt             # No dependencies (stdlib only!)
    ├── README.md                    # Setup & testing guide
    ├── Task_Division.md             # Module-wise responsibilities
    ├── Student_1_Script.md          # Presentation script (Blockchain)
    ├── Student_2_Script.md          # Presentation script (File Manager)
    ├── Student_3_Script.md          # Presentation script (Access Control)
    └── Student_4_Script.md          # Presentation script (Audit)
```

## 🎯 Projects Overview

### 1. DBMS Project: Startup Funding & Investor Matchmaking System
**Status**: ✅ **FULLY IMPLEMENTED & READY**

A complete database management system that connects startups with potential investors.

**Technology Stack**:
- Database: MySQL 5.7+
- Backend: Python Flask
- Security: bcrypt password hashing
- Architecture: 3-tier (Database → Application → Frontend)

**Features**:
- ✅ Normalized database schema (3NF)
- ✅ Complex matchmaking algorithm (JOIN queries)
- ✅ Stored procedures & functions
- ✅ User authentication & session management
- ✅ 10+ comprehensive analytical reports
- ✅ Sample data for immediate testing

**Quick Start**:
```bash
cd DBMS_Project
mysql -u root -p funding_system < database_schema.sql
pip install -r requirements.txt
python app.py
# Open http://localhost:5000
```

---

### 2. OS Project: Blockchain-Based File Access Control System
**Status**: ✅ **FULLY IMPLEMENTED & READY**

A secure file access control system using blockchain for immutable audit trails.

**Technology Stack**:
- Language: Pure Python 3.7+ (no external dependencies!)
- Blockchain: SHA256 hashing, chain validation
- Security: Role-Based Access Control (RBAC)
- Architecture: Modular design (4 independent modules)

**Features**:
- ✅ Complete blockchain implementation
- ✅ File operations (CREATE, READ, WRITE, DELETE)
- ✅ 3-tier RBAC (Admin, User, Guest)
- ✅ Immutable audit trail
- ✅ Tampering detection
- ✅ Security reports & analytics
- ✅ Interactive CLI + Demo mode

**Quick Start**:
```bash
cd OS_Project
python main.py --demo    # Automated demo
# OR
python main.py           # Interactive mode
```

## 📝 How to Use

1. **For Task Division**: Refer to `Task_Division.md` in each project folder for clear module assignments
2. **For Presentations**: Each student has a dedicated script file (2-3 minutes speaking time)
3. **For Viva/Demo**: Students can explain their specific module using the provided talking points

## ✅ Key Features

- **Even Distribution**: All students have equal workload and critical responsibilities
- **Clear Ownership**: Each student can independently explain their module
- **Faculty-Ready**: Structured for easy evaluation and marks distribution
- **Script-Based**: Ready-to-speak scripts for confident presentations

## 🎤 Presentation Tips

1. Memorize your key points (refer to your script)
2. Be ready to demo your specific module
3. Understand how your module connects with others
4. Prepare to answer 2-3 technical questions about your work
5. Practice timing: 2-3 minutes for introduction + demo time

---

**Date Created**: October 30, 2025  
**Purpose**: Academic Project Presentation & Evaluation

