"""
============================================
OS Project: Access Control & Security
Student 3: Role-Based Access Control (RBAC)
============================================
"""

from typing import Optional
from file_manager import User, UserManager, FileManager, FileMetadata
from blockchain import Blockchain
from datetime import datetime

# ============================================
# Permission Definitions
# ============================================

PERMISSIONS = {
    'Admin': {
        'CREATE': True,
        'READ': True,
        'WRITE': True,
        'DELETE': True
    },
    'User': {
        'CREATE': True,
        'READ': 'own_or_public',  # Can read own files or public files
        'WRITE': 'own',           # Can only write own files
        'DELETE': 'own'           # Can only delete own files
    },
    'Guest': {
        'CREATE': False,
        'READ': 'public',         # Can only read public files
        'WRITE': False,
        'DELETE': False
    }
}


class AccessControl:
    """Manages role-based access control"""
    
    def __init__(self, user_manager: UserManager, file_manager: FileManager, 
                 blockchain: Blockchain):
        """
        Initialize access control
        
        Args:
            user_manager: UserManager instance
            file_manager: FileManager instance
            blockchain: Blockchain for logging
        """
        self.user_manager = user_manager
        self.file_manager = file_manager
        self.blockchain = blockchain
    
    def check_permission(self, user_id: str, file_id: str, action: str) -> bool:
        """
        Check if user has permission to perform action on file
        
        Args:
            user_id: User attempting the action
            file_id: File to access
            action: Action to perform (CREATE, READ, WRITE, DELETE)
        
        Returns:
            True if allowed, False if denied
        """
        # Get user
        user = self.user_manager.get_user(user_id)
        if not user:
            print(f"✗ User not found: {user_id}")
            return False
        
        # Get file metadata
        file_meta = self.file_manager.get_file_metadata(file_id)
        
        # Special case for CREATE (file doesn't exist yet)
        if action == 'CREATE':
            return self._check_create_permission(user)
        
        # File must exist for other operations
        if not file_meta:
            print(f"✗ File not found: {file_id}")
            return False
        
        # Check permission based on role
        return self._check_role_permission(user, file_meta, action)
    
    def _check_create_permission(self, user: User) -> bool:
        """Check if user can create files"""
        permission = PERMISSIONS.get(user.role, {}).get('CREATE', False)
        return permission is True
    
    def _check_role_permission(self, user: User, file_meta: FileMetadata, 
                              action: str) -> bool:
        """
        Check permission based on role, ownership, and file permissions
        
        Args:
            user: User object
            file_meta: File metadata
            action: Action to perform
        
        Returns:
            True if allowed, False if denied
        """
        # Get role's permission for this action
        role_permission = PERMISSIONS.get(user.role, {}).get(action, False)
        
        # Case 1: Admin has full access
        if user.role == 'Admin':
            return True
        
        # Case 2: Guest permissions
        if user.role == 'Guest':
            if action == 'READ' and role_permission == 'public':
                # Guest can only read public files
                return file_meta.permissions == 'public'
            return False
        
        # Case 3: User permissions
        if user.role == 'User':
            # User owns the file
            if file_meta.owner_id == user.user_id:
                return role_permission in ['own', 'own_or_public', True]
            
            # User doesn't own the file
            if action == 'READ' and role_permission == 'own_or_public':
                # User can read public files
                return file_meta.permissions == 'public'
            
            return False
        
        # Default: deny
        return False
    
    def get_permission_summary(self, user_id: str) -> dict:
        """
        Get summary of what a user can do
        
        Returns:
            Dictionary with permissions summary
        """
        user = self.user_manager.get_user(user_id)
        if not user:
            return {"error": "User not found"}
        
        role_perms = PERMISSIONS.get(user.role, {})
        
        summary = {
            "user_id": user_id,
            "username": user.username,
            "role": user.role,
            "permissions": {
                "CREATE": self._describe_permission(role_perms.get('CREATE')),
                "READ": self._describe_permission(role_perms.get('READ')),
                "WRITE": self._describe_permission(role_perms.get('WRITE')),
                "DELETE": self._describe_permission(role_perms.get('DELETE'))
            }
        }
        
        return summary
    
    def _describe_permission(self, perm) -> str:
        """Convert permission value to human-readable description"""
        if perm is True:
            return "All files"
        elif perm is False:
            return "Not allowed"
        elif perm == 'own':
            return "Own files only"
        elif perm == 'public':
            return "Public files only"
        elif perm == 'own_or_public':
            return "Own files and public files"
        return "Unknown"
    
    def display_permission_matrix(self):
        """Display the complete permission matrix"""
        print("\n" + "="*70)
        print("ROLE-BASED ACCESS CONTROL (RBAC) PERMISSION MATRIX")
        print("="*70)
        
        print(f"\n{'Role':<10} {'CREATE':<20} {'READ':<20} {'WRITE':<20} {'DELETE':<20}")
        print("-" * 90)
        
        for role, perms in PERMISSIONS.items():
            print(f"{role:<10} ", end="")
            for action in ['CREATE', 'READ', 'WRITE', 'DELETE']:
                perm = perms.get(action, False)
                perm_str = self._describe_permission(perm)
                print(f"{perm_str:<20} ", end="")
            print()
        
        print("\n" + "="*70)
        print("Legend:")
        print("  • All files: Full access to any file")
        print("  • Own files only: Can only access files they created")
        print("  • Public files only: Can only access files marked as public")
        print("  • Own files and public files: Can access own files + public files")
        print("  • Not allowed: Cannot perform this action")
        print("="*70 + "\n")


# ============================================
# Security Validation Functions
# ============================================

def validate_user_id(user_id: str) -> bool:
    """Validate user ID format (alphanumeric only)"""
    return user_id.isalnum()


def validate_file_path(file_id: str) -> bool:
    """
    Validate file path to prevent directory traversal attacks
    
    Prevents: ../../../etc/passwd
    """
    # Check for directory traversal patterns
    if '..' in file_id or '/' in file_id or '\\' in file_id:
        return False
    return True


def sanitize_input(input_str: str) -> str:
    """Sanitize user input"""
    # Remove potentially dangerous characters
    dangerous_chars = ['<', '>', '|', '&', ';', '`', '$']
    for char in dangerous_chars:
        input_str = input_str.replace(char, '')
    return input_str


# ============================================
# Demo
# ============================================

if __name__ == "__main__":
    """Demo access control"""
    from blockchain import Blockchain
    from file_manager import UserManager, FileManager
    
    print("\n" + "="*70)
    print("DEMO: Role-Based Access Control")
    print("="*70 + "\n")
    
    # Initialize system
    bc = Blockchain()
    um = UserManager()
    fm = FileManager(bc, um)
    ac = AccessControl(um, fm, bc)
    
    # Set access control in file manager (circular dependency resolution)
    fm.access_control = ac
    
    # Display permission matrix
    ac.display_permission_matrix()
    
    # Create a private file
    print("=" * 70)
    print("Scenario 1: Admin creates private file")
    print("=" * 70)
    fm.create_file("secret.txt", "admin001", "Top secret data", "private")
    
    # Scenario 2: User tries to read admin's private file
    print("\n" + "=" * 70)
    print("Scenario 2: User tries to read admin's private file")
    print("=" * 70)
    content = fm.read_file("secret.txt", "user001")  # Should be denied
    
    # Scenario 3: Guest tries to read private file
    print("\n" + "=" * 70)
    print("Scenario 3: Guest tries to read admin's private file")
    print("=" * 70)
    content = fm.read_file("secret.txt", "guest001")  # Should be denied
    
    # Scenario 4: Create public file
    print("\n" + "=" * 70)
    print("Scenario 4: Admin creates public file")
    print("=" * 70)
    fm.create_file("public_data.txt", "admin001", "Public information", "public")
    
    # Scenario 5: Guest reads public file
    print("\n" + "=" * 70)
    print("Scenario 5: Guest reads public file")
    print("=" * 70)
    content = fm.read_file("public_data.txt", "guest001")  # Should succeed
    
    # Scenario 6: Guest tries to delete file
    print("\n" + "=" * 70)
    print("Scenario 6: Guest tries to delete file")
    print("=" * 70)
    fm.delete_file("public_data.txt", "guest001")  # Should be denied
    
    # Display blockchain with all access attempts
    bc.display_chain()
    
    # Show permission summaries
    print("\n" + "=" * 70)
    print("Permission Summaries")
    print("=" * 70)
    
    for user_id in ['admin001', 'user001', 'guest001']:
        summary = ac.get_permission_summary(user_id)
        print(f"\n{summary['username']} ({summary['role']}):")
        for action, perm in summary['permissions'].items():
            print(f"  {action}: {perm}")

