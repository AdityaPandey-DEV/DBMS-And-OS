# Student 3 – Access Control & Security
## Presentation Script (2-3 minutes)

---

## 🎤 Opening (15 seconds)

"Good morning/afternoon. I'm [Your Name], and I implemented the **Access Control and Security Module**. My code enforces role-based permissions and ensures only authorized users can access files."

---

## 📊 Main Presentation (2 minutes)

### 1. Role-Based Access Control (RBAC) (45 seconds)

"I designed a **Role-Based Access Control (RBAC) system** with three roles:

**Permission Matrix:**
```
┌────────┬────────┬──────┬───────┬────────┐
│  Role  │ Create │ Read │ Write │ Delete │
├────────┼────────┼──────┼───────┼────────┤
│ Admin  │   ✓    │  ✓   │   ✓   │   ✓    │ (Full access)
│ User   │   ✓    │ Own+ │  Own  │  Own   │ (Own files + read public)
│ Guest  │   ✗    │ Pub  │   ✗   │   ✗    │ (Read public only)
└────────┴────────┴──────┴───────┴────────┘

Legend:
- ✓ = Allowed for all files
- Own = Only their own files
- Own+ = Own files + public files
- Pub = Only public files
- ✗ = Not allowed
```

**Role Assignment:**
- Assigned during user registration
- Stored in User object: `user.role = 'Admin'`
- Cannot be self-modified (prevents privilege escalation)

This follows the **principle of least privilege** – users only get access they need."

### 2. Permission Check Implementation (45 seconds)

"I implemented the **check_permission() function** called before every file operation:

```python
def check_permission(user_id, file_id, action):
    user = get_user(user_id)
    file_info = get_file_metadata(file_id)
    
    # Admin has full access
    if user.role == 'Admin':
        return True
    
    # Guest can only read public files
    if user.role == 'Guest':
        if action == 'READ' and file_info['permissions'] == 'public':
            return True
        return False
    
    # User can access own files + read public files
    if user.role == 'User':
        if file_info['owner'] == user_id:  # Own file
            return True
        if action == 'READ' and file_info['permissions'] == 'public':
            return True
        return False
    
    return False  # Default deny
```

**Key Principles:**
1. **Default Deny**: If no rule matches, deny access
2. **Role-Based**: Decision depends on user's role
3. **Ownership**: Users control their own files
4. **Action-Specific**: Different permissions for READ vs WRITE"

### 3. Security Validation (30 seconds)

"I implemented **security measures** to prevent unauthorized access:

**1. User Authentication:**
- Before any operation, verify user_id is valid and logged in
- Check session hasn't expired
- Prevent session hijacking by validating session tokens

**2. Input Validation:**
- Sanitize file paths (prevent directory traversal attacks: `../../../etc/passwd`)
- Validate user_id format (must be alphanumeric)
- Check action is one of: CREATE, READ, WRITE, DELETE

**3. Privilege Escalation Prevention:**
- Users cannot change their own role
- Only Admin can promote User to Admin
- Role changes are logged to blockchain

**4. File Integrity:**
- Verify file exists before permission check
- Prevent race conditions (check-then-act attacks)"

### 4. Unauthorized Access Logging (30 seconds)

"Every **permission denial is logged to the blockchain**:

```python
def check_permission(user_id, file_id, action):
    allowed = perform_permission_check(...)
    
    if not allowed:
        # Log unauthorized attempt
        transaction = {
            'timestamp': datetime.now(),
            'user_id': user_id,
            'action': action,
            'file_id': file_id,
            'status': 'DENIED',
            'reason': 'Insufficient permissions'
        }
        blockchain.add_block(transaction)  # Student 1's function
    
    return allowed
```

**Why this matters:**
- Creates permanent record of security violations
- Helps identify malicious users or compromised accounts
- Provides evidence for audits and investigations
- Cannot be deleted by the attacker

Student 4 can query these logs to generate security reports like 'Top 10 users with most denied attempts'."

---

## 🎯 Closing (15 seconds)

"My access control module is the **security gatekeeper** of the system. I work with Student 2's file operations to enforce permissions and use Student 1's blockchain to log violations. Student 4 uses my logs for security audits. I can demonstrate permission checks for different roles. Thank you."

---

## 🔍 Potential Faculty Questions & Answers

### Q1: "What is Role-Based Access Control (RBAC)?"

**Answer**: "RBAC assigns permissions based on user roles, not individual users:

**Without RBAC** (difficult to manage):
- User1 can read File1, File2, File5
- User2 can read File1, write File3
- 100 users = 100 individual permission lists

**With RBAC** (easy to manage):
- Define roles once: Admin, User, Guest
- Assign users to roles
- All 'Users' automatically get same permissions

**Advantages:**
1. **Scalability**: Adding new users is simple – just assign a role
2. **Consistency**: All users with same role have identical permissions
3. **Maintenance**: Change permissions for entire role at once
4. **Principle of Least Privilege**: Users get only what their role requires

In our system: Admin (full access), User (own files), Guest (read-only public)."

### Q2: "How do you prevent unauthorized access?"

**Answer**: "I use a **two-layer security model**:

**Layer 1: Authentication (Who are you?)**
- User must log in with valid credentials
- Session created and validated before any operation
- Prevents impersonation

**Layer 2: Authorization (What can you do?)**
- My check_permission() function validates the action
- Checks role + ownership + file permissions
- Denies access if any check fails

**Example Flow:**
```
User 'guest007' tries to DELETE 'admin_file.txt'

Authentication: ✓ (guest007 is logged in)
Authorization: 
  - Is guest007 an Admin? ✗
  - Does guest007 own the file? ✗
  - Can Guests delete? ✗
Result: DENIED → Logged to blockchain
```

Both layers must pass for access to be granted."

### Q3: "What is the principle of least privilege?"

**Answer**: "**Principle of Least Privilege**: Give users the minimum permissions needed to do their job.

**In our system:**
- **Guest**: Only reads public files (can't create/modify anything)
  - Why? Guests are untrusted visitors
- **User**: Can create own files and read public files
  - Why? They need to work with their own data
- **Admin**: Full access to all files
  - Why? They manage the system

**Why it matters:**
1. **Limits damage**: If a Guest account is hacked, attacker can't delete files
2. **Reduces errors**: Users can't accidentally delete important files
3. **Compliance**: Many regulations (HIPAA, SOC2) require least privilege
4. **Audit trail**: Easier to track who did what

Example: A company intern (Guest) doesn't need delete access to company files."

### Q4: "Show me a permission check scenario."

**Answer**: "Let me walk through a complex scenario:

**Scenario**: User 'user001' (role: User) tries to WRITE to 'report.txt' owned by 'admin001'

**My check_permission() logic:**
```python
# Step 1: Get user and file info
user = get_user('user001')  # role='User'
file_info = get_file_metadata('report.txt')  # owner='admin001', permissions='private'

# Step 2: Check if Admin (skip other checks)
if user.role == 'Admin':
    return True  # ✗ user001 is not Admin

# Step 3: Check if User owns the file
if file_info['owner'] == 'user001':
    return True  # ✗ owner is admin001, not user001

# Step 4: Check if file is public and action is READ
if action == 'READ' and file_info['permissions'] == 'public':
    return True  # ✗ action is WRITE, and file is private

# Step 5: Default deny
return False  # ✗ DENIED
```

**Result**: Permission denied → User001 cannot write to admin's file → Denial logged to blockchain"

### Q5: "Why log denied access attempts?"

**Answer**: "Logging denied attempts is critical for **security monitoring**:

**1. Intrusion Detection:**
```
Block 50: guest007 attempts DELETE on passwords.txt → DENIED
Block 51: guest007 attempts READ on passwords.txt → DENIED
Block 52: guest007 attempts WRITE on passwords.txt → DENIED
```
Pattern shows potential attack – admin can investigate

**2. Insider Threat Detection:**
- Employee trying to access HR salary files → raises red flag
- Multiple failed attempts suggest intentional snooping

**3. Compliance & Audit:**
- Regulations require logging all access (successful and failed)
- Provides evidence: 'Who tried to access patient records?'

**4. Forensics:**
- If data breach occurs, blockchain shows exactly who attempted access
- Immutable logs can't be erased by attacker

**5. Accountability:**
- Users know attempts are logged → deterrent effect
- Can't deny unauthorized access attempt

Without logging denials, we'd only know successful operations – missing half the security picture!"

---

## 📋 Quick Reference Points

**Your Module**: Access Control & Security (RBAC, Permissions, Logging)  
**Key Skills Demonstrated**: Security Engineering, RBAC, Authentication/Authorization  
**Connection to Others**: Called by Student 2 for permission checks, logs to Student 1's blockchain

**Be Ready to Show**:
1. Permission matrix (table showing role permissions)
2. check_permission() function
3. Example of denied access scenario
4. How you log to blockchain
5. Security validation code

---

## 💡 Demo Flow (30 seconds)

1. "Admin logs in → tries to READ 'file.txt' → check_permission returns True → allowed"
2. "Guest logs in → tries to DELETE 'file.txt' → check_permission returns False → denied"
3. "Denied attempt logged to blockchain: `{'user': 'guest001', 'action': 'DELETE', 'status': 'DENIED'}`"
4. "Later, Student 4 queries blockchain → shows 'guest001 attempted unauthorized delete'"

---

**Confidence Tips**:
✓ Emphasize you're the "security gatekeeper"  
✓ Use the permission matrix to explain roles  
✓ Walk through check_permission() step-by-step  
✓ Use terms: RBAC, authentication, authorization, least privilege, default deny  
✓ Explain the "why" behind security decisions

