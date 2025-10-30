# OS Project: Blockchain-Based File Access Control System

A secure file access control system using blockchain technology for immutable audit trails with role-based access control (RBAC).

## 📁 Project Structure

```
OS_Project/
├── blockchain.py          # Student 1: Blockchain core implementation
├── file_manager.py        # Student 2: File & user management
├── access_control.py      # Student 3: RBAC & security
├── audit_reports.py       # Student 4: Audit & reporting
├── main.py               # Integrated main application
├── requirements.txt      # Python dependencies
├── files/                # Directory for managed files (auto-created)
└── README.md            # This file
```

## 🚀 Quick Start

### Prerequisites

1. **Python** (version 3.7+)
2. **pip** (Python package manager)

### Installation Steps

#### Step 1: Install Dependencies

```bash
# Install required packages (only standard library modules used!)
# No external dependencies needed - project uses only Python built-ins
```

This project intentionally uses **only Python standard library** to demonstrate:
- Pure Python implementation
- No external dependencies
- Easy deployment

#### Step 2: Run the System

**Option A: Interactive Mode (Menu-driven)**
```bash
python main.py
```

**Option B: Demo Mode (Automated demonstration)**
```bash
python main.py --demo
```

#### Step 3: Explore Individual Modules

Test each student's module independently:

```bash
# Test Student 1: Blockchain
python blockchain.py

# Test Student 2: File Manager
python file_manager.py

# Test Student 3: Access Control
python access_control.py

# Test Student 4: Audit Reports
python audit_reports.py
```

## 📊 Testing the Project

### Test Student 1 (Blockchain Core)

```bash
python blockchain.py
```

**What it demonstrates**:
- Genesis block creation
- Adding new blocks
- SHA256 hash calculation
- Chain validation
- Tampering detection

**Expected output**:
```
✓ Genesis block created: 0000000000000000...
Block 1 added: User1 created file.txt
Block 2 added: User2 read file.txt
✓ Blockchain is VALID
--- After tampering ---
✗ Blockchain is INVALID - Tampering detected!
```

### Test Student 2 (File & User Management)

```bash
python file_manager.py
```

**What it demonstrates**:
- User registration (Admin, User, Guest)
- File creation (CREATE)
- File reading (READ)
- File writing (WRITE)
- File deletion (DELETE)
- Blockchain logging for each operation

**Expected output**:
```
✓ User registered: Admin (Admin)
✓ File created: test.txt by admin001
✓ File read: test.txt by admin001
--- Blockchain logs all operations ---
```

### Test Student 3 (Access Control)

```bash
python access_control.py
```

**What it demonstrates**:
- RBAC permission matrix
- Admin: Full access
- User: Own files + read public
- Guest: Read public only
- Permission checks before operations
- Denied access logging

**Expected output**:
```
Permission Matrix:
  Admin  → Full access to all files
  User   → Own files + public files
  Guest  → Public files only (read-only)

Scenario: Guest tries to delete file
  ✗ Access denied
  → Logged to blockchain as DENIED
```

### Test Student 4 (Audit & Reporting)

```bash
python audit_reports.py
```

**What it demonstrates**:
- File access history queries
- User activity reports
- Security violations report
- System statistics
- Export to JSON/CSV

**Expected output**:
```
FILE ACCESS REPORT: report.txt
───────────────────────────────────────
Timestamp            User      Action   Status
2025-10-30 10:15:23  admin001  CREATE   SUCCESS
2025-10-30 11:20:45  user001   READ     DENIED
───────────────────────────────────────

SECURITY REPORT: 3 unauthorized attempts detected
  • guest001: 2 violations
  • user001: 1 violation
```

### Test Complete System (All Modules Integrated)

```bash
# Run automated demo
python main.py --demo
```

This will:
1. Initialize all modules
2. Create sample users (Admin, User, Guest)
3. Perform various file operations
4. Demonstrate access control
5. Generate comprehensive reports
6. Display blockchain with all transactions

## 🎓 Student Responsibilities

### Student 1: Blockchain Core Developer
**File**: `blockchain.py`

**What to demonstrate**:
```python
# 1. Show Block class
block = Block(index=1, timestamp="...", data={...}, previous_hash="...")

# 2. Show hash calculation
hash = block.calculate_hash()  # SHA256

# 3. Show chain validation
is_valid = blockchain.validate_chain()  # Returns True/False

# 4. Demonstrate tampering detection
blockchain.chain[1].data['user'] = 'hacker'  # Tamper
blockchain.validate_chain()  # Returns False - tampering detected!
```

**Key points**:
- Each block contains: index, timestamp, data, previous_hash, hash
- SHA256 ensures immutability
- Chain validation detects any modifications
- Genesis block is the first block (previous_hash = "0")

### Student 2: File & User Management
**File**: `file_manager.py`

**What to demonstrate**:
```python
# 1. User Management
um = UserManager()
um.register_user('user001', 'Alice', 'User')

# 2. File Operations
fm = FileManager(blockchain, user_manager)
fm.create_file('test.txt', 'user001', 'content')
fm.read_file('test.txt', 'user001')
fm.write_file('test.txt', 'user001', 'new content')
fm.delete_file('test.txt', 'user001')

# 3. Show blockchain logging
# Every operation adds a block with transaction details
```

**Key points**:
- Three roles: Admin, User, Guest
- Every file operation logged to blockchain
- Metadata stores: owner, permissions, timestamps
- File permissions: private or public

### Student 3: Access Control & Security
**File**: `access_control.py`

**What to demonstrate**:
```python
# 1. Permission Matrix
ac = AccessControl(user_manager, file_manager, blockchain)
ac.display_permission_matrix()

# 2. Permission Check
allowed = ac.check_permission(user_id='guest001', 
                              file_id='admin_file.txt', 
                              action='DELETE')
# Returns False - Guest cannot delete

# 3. Show denied access logging
# Failed attempts are logged to blockchain for audit
```

**Key points**:
- **Admin**: Full access (all operations on all files)
- **User**: Own files + read public files
- **Guest**: Read-only access to public files
- All denials logged to blockchain (permanent record)
- Principle of least privilege

### Student 4: Audit & Reporting
**File**: `audit_reports.py`

**What to demonstrate**:
```python
# 1. Query file access history
reporter = AuditReporter(blockchain, user_manager)
history = reporter.query_file_access('report.txt')

# 2. Query user activity
activity = reporter.query_user_activity('admin001')

# 3. Security violations report
violations = reporter.query_denied_access()

# 4. Generate formatted reports
reporter.generate_file_access_report('report.txt')
reporter.generate_security_report()
reporter.generate_summary_statistics()

# 5. Export to files
reporter.export_blockchain_to_csv('blockchain_audit.csv')
```

**Key points**:
- Query blockchain by: file, user, action, time range
- Generate formatted reports
- Identify security violations
- Export to JSON/CSV for analysis
- Cannot delete or modify logs (immutability)

## 🎮 Interactive System (Main Application)

```bash
python main.py
```

**Main Menu Options**:
1. **Login** - Login as Admin/User/Guest
2. **Create File** - Create new file (if permitted)
3. **Read File** - Read file contents (if permitted)
4. **Write File** - Modify file (if permitted)
5. **Delete File** - Remove file (if permitted)
6. **List Files** - Show all files in system
7. **View My Permissions** - See what you can do
8. **Generate Reports** - Audit reports menu
9. **View Blockchain** - Display entire blockchain
10. **Validate Blockchain** - Check integrity
11. **Logout** - Logout current user
0. **Exit** - Close system

## 🔍 Sample Demo Flow

```bash
python main.py --demo
```

**What happens**:

1. **System Initialization**
   - Creates blockchain with genesis block
   - Registers 3 default users:
     - admin001 (Admin role)
     - user001 (User role)
     - guest001 (Guest role)

2. **Scenario 1: Admin Operations**
   ```
   Login as: admin001 (Admin)
   ✓ Create private file: admin_report.txt
   ✓ Create public file: public_notice.txt
   All logged to blockchain
   ```

3. **Scenario 2: User Operations**
   ```
   Login as: user001 (User)
   ✓ Create own file: my_notes.txt
   ✓ Read public file: public_notice.txt (allowed)
   ✗ Read private file: admin_report.txt (denied → logged)
   ```

4. **Scenario 3: Guest Operations**
   ```
   Login as: guest001 (Guest)
   ✓ Read public file: public_notice.txt (allowed)
   ✗ Read private file: admin_report.txt (denied → logged)
   ✗ Delete file: public_notice.txt (denied → logged)
   ```

5. **Report Generation**
   - File access history
   - Security violations (3 denied attempts)
   - System statistics
   - Blockchain visualization

## 🔒 Security Features

1. **Immutable Audit Trail**
   - All operations permanently logged
   - Cannot delete or modify history
   - Blockchain validation detects tampering

2. **Role-Based Access Control**
   - Principle of least privilege
   - Clear permission boundaries
   - Hierarchical roles

3. **Security Monitoring**
   - Unauthorized attempts logged
   - Identify malicious users
   - Pattern detection

4. **Input Validation**
   - Prevent directory traversal (../../../etc/passwd)
   - Alphanumeric user IDs only
   - Sanitized inputs

## 📝 Project Files Generated

When you run the system, it creates:

```
OS_Project/
├── blockchain.json          # Blockchain state (can be loaded/saved)
├── users.json              # User database
├── file_metadata.json      # File ownership & permissions
├── files/                  # Actual file storage
│   ├── test.txt
│   ├── report.txt
│   └── ...
├── security_report.json    # Exported security report
└── blockchain_audit.csv    # Exported audit trail
```

## 🎤 Presentation Tips

### Demo Flow (10 minutes):

**Minutes 1-2**: Student 1
- Show blockchain structure
- Demonstrate hash calculation
- Prove tampering detection

**Minutes 3-4**: Student 2
- Show file operations
- Demonstrate blockchain logging
- Show user management

**Minutes 5-6**: Student 3
- Display permission matrix
- Demo access control
- Show denied access logging

**Minutes 7-8**: Student 4
- Generate reports
- Show security violations
- Display blockchain

**Minutes 9-10**: Integration
- Run complete demo
- Show all modules working together
- Q&A

## 🎯 Key Features

✓ **Pure Python** - No external dependencies  
✓ **Blockchain** - Immutable transaction log  
✓ **RBAC** - Three-tier access control  
✓ **Audit Trail** - Complete history tracking  
✓ **Tamper Detection** - Cryptographic validation  
✓ **Security Reports** - Violation tracking  
✓ **Modular Design** - Clear separation of concerns  
✓ **Interactive CLI** - User-friendly interface  

## 🐛 Troubleshooting

**Issue 1: Permission denied when creating files**
```
✗ Access denied: user001 cannot create file
```
**Solution**: Check user role. Only Admin and User can create files. Guest is read-only.

**Issue 2: Files directory not found**
```
FileNotFoundError: [Errno 2] No such file or directory: './files/test.txt'
```
**Solution**: Directory auto-creates on first run. If deleted, restart the program.

**Issue 3: Blockchain validation fails**
```
✗ Blockchain is INVALID
```
**Solution**: This means blockchain was tampered with (intentional for demo). Restart system or reload from blockchain.json.

## 📚 Concepts Demonstrated

### Operating System Concepts:
- File management
- Access control
- User authentication
- Audit logging
- Security policies

### Blockchain Concepts:
- Distributed ledger (simplified)
- Cryptographic hashing
- Immutability
- Chain validation
- Tamper detection

### Software Engineering:
- Modular design
- Separation of concerns
- Clear interfaces
- Comprehensive testing

## 🎯 Evaluation Points

Each student can independently explain:

**Student 1**: 
- How blockchain works
- Why immutability matters
- How tampering is detected
- SHA256 hash function

**Student 2**: 
- File operation implementation
- User management system
- Blockchain integration
- Metadata storage

**Student 3**: 
- RBAC design principles
- Permission checking logic
- Security validation
- Least privilege principle

**Student 4**: 
- Blockchain query methods
- Report generation
- Data export functionality
- System integration

---

**Date Created**: October 30, 2025  
**Team Members**: 4 students  
**Language**: Python 3.7+  
**Dependencies**: None (stdlib only)  
**Platform**: Cross-platform (Windows/Mac/Linux)

