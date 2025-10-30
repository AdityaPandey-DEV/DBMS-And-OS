# OS Project: Blockchain-Based File Access Control System
## Task Division (4 Students)

---

## 👤 Student 1 – Blockchain Core Developer

### Primary Responsibilities:
1. **Blockchain Structure Design**
   - Implemented Block class with attributes: index, timestamp, data, previous_hash, hash
   - Created Blockchain class to manage the chain
   - Designed data structure for storing blocks in memory/file

2. **Hashing Mechanism**
   - Implemented SHA256 hashing algorithm
   - Created hash calculation function that takes block data as input
   - Ensured each block's hash depends on its content and previous block's hash

3. **Block Creation**
   - Wrote function to create genesis block (first block)
   - Implemented add_block() function to append new blocks
   - Each block includes: block_index, timestamp, transaction_data, prev_hash, current_hash

4. **Chain Validation**
   - Created validate_chain() function to verify blockchain integrity
   - Checks: hash values are correct, previous_hash matches, chain is not tampered
   - Returns True if chain is valid, False otherwise

5. **Immutability Testing**
   - Tested tampering scenarios (modifying old block data)
   - Verified that validation fails when chain is tampered
   - Demonstrated blockchain's core security feature

### Deliverables:
- Blockchain implementation code (Python/Java/C++)
- Block and Blockchain class definitions
- Hash calculation module
- Chain validation function
- Test cases showing tamper detection

---

## 👤 Student 2 – File & User Management

### Primary Responsibilities:
1. **User Management System**
   - Created User class with attributes: user_id, username, role (Admin/User/Guest)
   - Implemented user registration and login (basic authentication)
   - Stored user data in a file/database

2. **File Operations Implementation**
   - **Create**: Function to create new files with owner information
   - **Read**: Function to read file contents (permission-based)
   - **Write**: Function to write/append to files (permission-based)
   - **Delete**: Function to delete files (admin/owner only)

3. **File Metadata Management**
   - Tracked file owner (who created the file)
   - Stored file permissions (who can access)
   - Maintained file timestamps (created, last modified)

4. **Blockchain Integration**
   - Every file operation (create/read/write/delete) generates a transaction
   - Transaction includes: file_id, user_id, action, timestamp
   - Calls Student 1's add_block() to log the transaction in blockchain

5. **File System Structure**
   - Organized files in a directory structure
   - Implemented file_id system for tracking
   - Ensured smooth integration with access control module

### Deliverables:
- User management code
- File operation functions (create, read, write, delete)
- Transaction logging mechanism
- Integration code with blockchain module
- Sample file system with test files

---

## 👤 Student 3 – Access Control & Security

### Primary Responsibilities:
1. **Role-Based Access Control (RBAC)**
   - Defined three roles: **Admin**, **User**, **Guest**
   - Created permission matrix for each role
   - Implemented role assignment during user registration

2. **Permission Definitions**
   - **Admin**: Full access (create, read, write, delete any file)
   - **User**: Can create files, read/write own files, read others' public files
   - **Guest**: Read-only access to public files

3. **Access Control Logic**
   - Implemented check_permission() function
   - Called before every file operation
   - Validates: Does user have permission for this action on this file?

4. **Security Validation**
   - User authentication before any file access
   - Prevents unauthorized access attempts
   - Validates user identity using user_id and session

5. **Audit Trail (Blockchain Logging)**
   - Logged all access attempts (successful and failed) to blockchain
   - Transaction format: {user_id, file_id, action, status: "allowed"/"denied", timestamp}
   - Unauthorized attempts are permanently recorded for audit

### Deliverables:
- RBAC implementation code
- Permission matrix documentation
- check_permission() function
- Security validation module
- Blockchain integration for unauthorized access logging
- Test cases for different permission scenarios

---

## 👤 Student 4 – Audit & Reporting Module

### Primary Responsibilities:
1. **Blockchain Query Functions**
   - **Who accessed file X?** – Query blockchain for all transactions involving a specific file_id
   - **What did user Y do?** – Query all actions performed by a specific user_id
   - **Show all unauthorized attempts** – Filter transactions where status = "denied"
   - **Timeline of actions** – Display chronological history of file operations

2. **Report Generation**
   - Created report templates for different queries
   - Formatted blockchain data into readable tables
   - Generated CSV/PDF reports from blockchain logs
   - Summary statistics: total operations, most active users, most accessed files

3. **Blockchain Visualization**
   - Created visual representation of blockchain
   - Displayed: Block Index → Hash → Previous Hash → Data
   - Showed chain structure as linked blocks
   - Simple console output or graphical representation

4. **System Documentation**
   - Advantages: Immutable audit trail, tamper-proof logs, transparency
   - Limitations: Performance overhead, storage requirements, no privacy
   - Future Scope: Distributed blockchain, smart contracts, encryption

5. **Integration & Testing**
   - Coordinated all modules: blockchain + file system + access control + audit
   - End-to-end testing: user logs in → performs file operation → logged in blockchain → query shows record
   - Created demo scenarios for presentation
   - Prepared presentation slides and documentation

### Deliverables:
- Query functions for blockchain analysis
- Report generation code
- Blockchain visualization tool
- Complete project documentation
- Presentation slides
- Demo flow and test scenarios

---

## 🔗 Module Dependencies

```
Student 1 (Blockchain) ← Student 2 (File Ops) → Student 3 (Access Control)
          ↓                        ↓                       ↓
     All feed into Student 4 (Audit & Reports)
```

**Data Flow:**
1. User attempts file operation (Student 2)
2. Access control checks permission (Student 3)
3. If allowed, operation executes; transaction created (Student 2)
4. Transaction added to blockchain (Student 1)
5. Audit queries retrieve transaction history (Student 4)

---

## 🔒 Key Technical Concepts Covered

**Operating System Concepts:**
- File Management (create, read, write, delete)
- Access Control (permissions, roles)
- Security (authentication, authorization)
- Audit Trails (logging)

**Blockchain Concepts:**
- Immutability (tamper-proof records)
- Hashing (SHA256)
- Chain structure (linked blocks)
- Validation (integrity checks)

---

## ✅ Evaluation Points

Each student can independently explain:
- **What** they built (their specific module)
- **How** they implemented it (code walkthrough)
- **Why** blockchain is useful for file access control (immutability, audit)
- **How** their module integrates with others
- **Challenges** faced and solutions

---

**Note**: All students should understand basic blockchain and file system concepts, but have deep expertise in their assigned module.

