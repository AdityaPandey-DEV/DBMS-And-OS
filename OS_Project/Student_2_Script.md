# Student 2 – File & User Management
## Presentation Script (2-3 minutes)

---

## 🎤 Opening (15 seconds)

"Good morning/afternoon. I'm [Your Name], and I developed the **File and User Management System**. I implemented all file operations and integrated them with the blockchain for logging."

---

## 📊 Main Presentation (2 minutes)

### 1. User Management (30 seconds)

"I created a **User Management System** with three components:

**User Class:**
```python
class User:
    def __init__(self, user_id, username, role):
        self.user_id = user_id
        self.username = username
        self.role = role  # 'Admin', 'User', or 'Guest'
```

**User Registration:**
- Collects username and assigns a unique user_id
- Assigns role (Admin/User/Guest)
- Stores user information in a file (users.json)

**User Login:**
- Validates username and user_id
- Creates a session for the logged-in user
- All subsequent file operations are performed by this authenticated user"

### 2. File Operations (45 seconds)

"I implemented **four core file operations**, each integrated with the blockchain:

**1. CREATE:**
```python
def create_file(filename, owner_id):
    # Create the physical file
    with open(filename, 'w') as f:
        f.write('')
    # Log to blockchain
    transaction = {'action': 'CREATE', 'file': filename, 'user': owner_id}
    blockchain.add_block(transaction)
```

**2. READ:**
- Opens file and returns contents
- Checks permission (calls Student 3's check_permission)
- Logs: `{'action': 'READ', 'file': filename, 'user': user_id}`

**3. WRITE:**
- Appends or overwrites file content
- Permission-based (only owner or admin)
- Logs: `{'action': 'WRITE', 'file': filename, 'user': user_id, 'data': content}`

**4. DELETE:**
- Removes file from system
- Admin or owner only
- Logs: `{'action': 'DELETE', 'file': filename, 'user': user_id}`

**Every operation creates a transaction** that gets added to Student 1's blockchain."

### 3. File Metadata Management (30 seconds)

"I maintain **file metadata** for access control:

**File Metadata Structure:**
```python
{
    'file.txt': {
        'owner': 'user001',
        'created': '2025-10-30 10:15:00',
        'last_modified': '2025-10-30 11:20:00',
        'permissions': 'private'  # 'private' or 'public'
    }
}
```

This metadata is used by Student 3's access control module to determine:
- Who owns the file?
- Is it public (readable by all) or private?
- When was it last accessed?

Metadata is stored separately from the blockchain but referenced during permission checks."

### 4. Blockchain Integration (30 seconds)

"The **key innovation** is that **every file operation is logged to the blockchain**:

**Transaction Format:**
```python
transaction = {
    'timestamp': '2025-10-30 10:15:23',
    'user_id': 'user001',
    'action': 'READ',
    'file_id': 'file.txt',
    'status': 'SUCCESS'
}
blockchain.add_block(transaction)  # Calls Student 1's function
```

**Flow:**
1. User calls `read_file('file.txt')`
2. My code checks permission (calls Student 3's function)
3. If allowed → perform read → log 'SUCCESS' to blockchain
4. If denied → log 'DENIED' to blockchain

This creates an **immutable audit trail** – every file access is permanently recorded."

---

## 🎯 Closing (15 seconds)

"My file management module bridges the operating system's file operations with blockchain logging. I use Student 1's blockchain to log transactions and Student 3's access control to enforce permissions. Student 4 queries my transaction logs for audit reports. I can demonstrate any file operation. Thank you."

---

## 🔍 Potential Faculty Questions & Answers

### Q1: "How do you integrate file operations with blockchain?"

**Answer**: "After every file operation, I create a transaction dictionary and call Student 1's add_block() function:

```python
def read_file(filename, user_id):
    # Step 1: Check permission (Student 3's function)
    if not check_permission(user_id, filename, 'READ'):
        transaction = {'user': user_id, 'action': 'READ', 'file': filename, 'status': 'DENIED'}
        blockchain.add_block(transaction)
        return 'Access Denied'
    
    # Step 2: Perform operation
    with open(filename, 'r') as f:
        content = f.read()
    
    # Step 3: Log to blockchain
    transaction = {'user': user_id, 'action': 'READ', 'file': filename, 'status': 'SUCCESS'}
    blockchain.add_block(transaction)
    
    return content
```

The blockchain automatically links this transaction to the chain, making it tamper-proof."

### Q2: "What's the difference between file metadata and blockchain logs?"

**Answer**: 
"**File Metadata** (stored in memory/file):
- Current state: Who owns the file right now? When was it created?
- Can be updated: If ownership transfers, metadata changes
- Used for permission checks

**Blockchain Logs** (immutable chain):
- Historical record: Every action that was ever performed
- Cannot be updated: Permanent history
- Used for audit trails

Example:
- Metadata: `file.txt` is owned by User1
- Blockchain: Shows User1 created it (Block 5), User2 read it (Block 7), User1 deleted it (Block 10)

Metadata tells the current state, blockchain tells the complete history."

### Q3: "How do you handle file permissions?"

**Answer**: "I work with Student 3's access control module:

**Step 1**: User requests file operation  
**Step 2**: I call `check_permission(user_id, file_id, action)`  
**Step 3**: Student 3's function checks:
- What's the user's role? (Admin/User/Guest)
- Does user own the file?
- Is the file public or private?

**Step 4**: Returns True/False  
**Step 5**: If True → I perform operation; If False → I deny and log to blockchain

Example:
```python
if check_permission('user001', 'file.txt', 'WRITE'):
    # Allow write operation
else:
    # Deny and log 'UNAUTHORIZED ATTEMPT' to blockchain
```

This separation of concerns makes the system modular – I handle file operations, Student 3 handles permission logic."

### Q4: "Why log denied operations to blockchain?"

**Answer**: "Logging denied operations is crucial for **security auditing**:

**1. Detect intrusion attempts**: If Guest123 tries to delete admin files 50 times, that's suspicious
**2. Accountability**: Can't hide unauthorized access attempts – they're permanently recorded
**3. Forensics**: If data is stolen, we can trace who attempted access and when
**4. Compliance**: Many regulations require logging all access attempts (HIPAA, GDPR)

Example blockchain log:
```
Block 15: User 'guest007' attempted DELETE on 'admin_passwords.txt' → DENIED
Block 16: User 'guest007' attempted READ on 'admin_passwords.txt' → DENIED
Block 17: User 'guest007' attempted WRITE on 'admin_passwords.txt' → DENIED
```

This shows a pattern of malicious behavior – admins can investigate."

### Q5: "Show me the file creation process."

**Answer**: "Here's the complete flow when Admin creates a file:

**Step 1: User calls create_file()**
```python
create_file('report.txt', owner_id='admin001')
```

**Step 2: My function creates the physical file**
```python
with open('report.txt', 'w') as f:
    f.write('')  # Empty file
```

**Step 3: Store metadata**
```python
file_metadata['report.txt'] = {
    'owner': 'admin001',
    'created': datetime.now(),
    'permissions': 'private'
}
```

**Step 4: Log to blockchain**
```python
transaction = {
    'timestamp': '2025-10-30 10:15:23',
    'user_id': 'admin001',
    'action': 'CREATE',
    'file_id': 'report.txt',
    'status': 'SUCCESS'
}
blockchain.add_block(transaction)
```

Now the file exists on disk, metadata is stored, and the creation is permanently logged in blockchain."

---

## 📋 Quick Reference Points

**Your Module**: File Operations + User Management + Blockchain Integration  
**Key Skills Demonstrated**: File I/O, User Authentication, System Integration  
**Connection to Others**: Use Student 1's blockchain, call Student 3's permissions, provide data to Student 4

**Be Ready to Show**:
1. One file operation function (create/read/write/delete)
2. User class definition
3. How you call blockchain.add_block()
4. File metadata structure
5. Transaction format

---

## 💡 Demo Flow (30 seconds)

1. "User 'admin001' logs in"
2. "Calls create_file('test.txt') → file created on disk"
3. "Transaction logged: `{'action': 'CREATE', 'file': 'test.txt', 'user': 'admin001'}`"
4. "User 'guest001' tries to delete 'test.txt' → permission denied (Student 3)"
5. "Denied attempt logged: `{'action': 'DELETE', 'file': 'test.txt', 'user': 'guest001', 'status': 'DENIED'}`"
6. "Both transactions now in blockchain → permanent audit trail"

---

**Confidence Tips**:
✓ Focus on the flow: operation → permission check → execute → log  
✓ Emphasize: "Every action is logged to blockchain"  
✓ Use terms: transaction, metadata, blockchain integration, audit trail  
✓ Show how your module connects Student 1 and Student 3  
✓ Have sample transaction JSON ready to show

