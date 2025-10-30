"""
============================================
OS Project: File & User Management
Student 2: File Operations & Blockchain Integration
============================================
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional
from blockchain import Blockchain

# ============================================
# User Management
# ============================================

class User:
    """Represents a user in the system"""
    
    def __init__(self, user_id: str, username: str, role: str):
        """
        Initialize a user
        
        Args:
            user_id: Unique identifier
            username: Display name
            role: 'Admin', 'User', or 'Guest'
        """
        self.user_id = user_id
        self.username = username
        self.role = role
    
    def to_dict(self) -> Dict:
        """Convert user to dictionary"""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "role": self.role
        }
    
    def __repr__(self) -> str:
        return f"User(id={self.user_id}, name={self.username}, role={self.role})"


class UserManager:
    """Manages user accounts"""
    
    def __init__(self):
        """Initialize user manager"""
        self.users: Dict[str, User] = {}
        self.load_users()
    
    def register_user(self, user_id: str, username: str, role: str) -> User:
        """Register a new user"""
        if user_id in self.users:
            raise ValueError(f"User {user_id} already exists")
        
        if role not in ['Admin', 'User', 'Guest']:
            raise ValueError(f"Invalid role: {role}")
        
        user = User(user_id, username, role)
        self.users[user_id] = user
        self.save_users()
        
        print(f"✓ User registered: {username} ({role})")
        return user
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return self.users.get(user_id)
    
    def save_users(self):
        """Save users to file"""
        users_data = {uid: user.to_dict() for uid, user in self.users.items()}
        with open('users.json', 'w') as f:
            json.dump(users_data, f, indent=2)
    
    def load_users(self):
        """Load users from file"""
        try:
            with open('users.json', 'r') as f:
                users_data = json.load(f)
            
            for user_id, user_dict in users_data.items():
                self.users[user_id] = User(**user_dict)
        except FileNotFoundError:
            # Create default users
            self.register_user('admin001', 'Admin', 'Admin')
            self.register_user('user001', 'Alice', 'User')
            self.register_user('guest001', 'Bob', 'Guest')


# ============================================
# File Management
# ============================================

class FileMetadata:
    """Stores metadata about files"""
    
    def __init__(self, file_id: str, owner_id: str, permissions: str = 'private'):
        self.file_id = file_id
        self.owner_id = owner_id
        self.permissions = permissions  # 'private' or 'public'
        self.created = datetime.now().isoformat()
        self.last_modified = self.created
    
    def to_dict(self) -> Dict:
        return {
            "file_id": self.file_id,
            "owner_id": self.owner_id,
            "permissions": self.permissions,
            "created": self.created,
            "last_modified": self.last_modified
        }


class FileManager:
    """Manages file operations with blockchain logging"""
    
    def __init__(self, blockchain: Blockchain, user_manager: UserManager, 
                 access_control=None, files_dir: str = "./files"):
        """
        Initialize file manager
        
        Args:
            blockchain: Blockchain instance for logging
            user_manager: UserManager instance
            access_control: AccessControl instance (set later to avoid circular import)
            files_dir: Directory to store files
        """
        self.blockchain = blockchain
        self.user_manager = user_manager
        self.access_control = access_control
        self.files_dir = files_dir
        self.metadata: Dict[str, FileMetadata] = {}
        
        # Create files directory
        os.makedirs(self.files_dir, exist_ok=True)
        self.load_metadata()
    
    def create_file(self, file_id: str, owner_id: str, content: str = "", 
                   permissions: str = 'private') -> bool:
        """
        Create a new file
        
        Args:
            file_id: Name of the file
            owner_id: User ID of the creator
            content: Initial file content
            permissions: 'private' or 'public'
        
        Returns:
            True if successful, False otherwise
        """
        file_path = os.path.join(self.files_dir, file_id)
        
        try:
            # Create the physical file
            with open(file_path, 'w') as f:
                f.write(content)
            
            # Store metadata
            self.metadata[file_id] = FileMetadata(file_id, owner_id, permissions)
            self.save_metadata()
            
            # Log to blockchain
            transaction = {
                "timestamp": datetime.now().isoformat(),
                "user_id": owner_id,
                "action": "CREATE",
                "file_id": file_id,
                "status": "SUCCESS"
            }
            self.blockchain.add_block(transaction)
            
            print(f"✓ File created: {file_id} by {owner_id}")
            return True
        
        except Exception as e:
            print(f"✗ File creation failed: {e}")
            
            # Log failure to blockchain
            transaction = {
                "timestamp": datetime.now().isoformat(),
                "user_id": owner_id,
                "action": "CREATE",
                "file_id": file_id,
                "status": "FAILED",
                "error": str(e)
            }
            self.blockchain.add_block(transaction)
            return False
    
    def read_file(self, file_id: str, user_id: str) -> Optional[str]:
        """Read file contents (with permission check)"""
        # Check permission
        if self.access_control and not self.access_control.check_permission(user_id, file_id, 'READ'):
            # Log denied attempt
            transaction = {
                "timestamp": datetime.now().isoformat(),
                "user_id": user_id,
                "action": "READ",
                "file_id": file_id,
                "status": "DENIED",
                "reason": "Insufficient permissions"
            }
            self.blockchain.add_block(transaction)
            print(f"✗ Access denied: {user_id} cannot read {file_id}")
            return None
        
        # Read file
        file_path = os.path.join(self.files_dir, file_id)
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            # Log success
            transaction = {
                "timestamp": datetime.now().isoformat(),
                "user_id": user_id,
                "action": "READ",
                "file_id": file_id,
                "status": "SUCCESS"
            }
            self.blockchain.add_block(transaction)
            
            print(f"✓ File read: {file_id} by {user_id}")
            return content
        
        except FileNotFoundError:
            print(f"✗ File not found: {file_id}")
            return None
    
    def write_file(self, file_id: str, user_id: str, content: str) -> bool:
        """Write/append to file (with permission check)"""
        # Check permission
        if self.access_control and not self.access_control.check_permission(user_id, file_id, 'WRITE'):
            # Log denied attempt
            transaction = {
                "timestamp": datetime.now().isoformat(),
                "user_id": user_id,
                "action": "WRITE",
                "file_id": file_id,
                "status": "DENIED",
                "reason": "Insufficient permissions"
            }
            self.blockchain.add_block(transaction)
            print(f"✗ Access denied: {user_id} cannot write to {file_id}")
            return False
        
        # Write to file
        file_path = os.path.join(self.files_dir, file_id)
        
        try:
            with open(file_path, 'w') as f:
                f.write(content)
            
            # Update metadata
            if file_id in self.metadata:
                self.metadata[file_id].last_modified = datetime.now().isoformat()
                self.save_metadata()
            
            # Log success
            transaction = {
                "timestamp": datetime.now().isoformat(),
                "user_id": user_id,
                "action": "WRITE",
                "file_id": file_id,
                "status": "SUCCESS",
                "content_length": len(content)
            }
            self.blockchain.add_block(transaction)
            
            print(f"✓ File written: {file_id} by {user_id}")
            return True
        
        except Exception as e:
            print(f"✗ Write failed: {e}")
            return False
    
    def delete_file(self, file_id: str, user_id: str) -> bool:
        """Delete file (with permission check)"""
        # Check permission
        if self.access_control and not self.access_control.check_permission(user_id, file_id, 'DELETE'):
            # Log denied attempt
            transaction = {
                "timestamp": datetime.now().isoformat(),
                "user_id": user_id,
                "action": "DELETE",
                "file_id": file_id,
                "status": "DENIED",
                "reason": "Insufficient permissions"
            }
            self.blockchain.add_block(transaction)
            print(f"✗ Access denied: {user_id} cannot delete {file_id}")
            return False
        
        # Delete file
        file_path = os.path.join(self.files_dir, file_id)
        
        try:
            os.remove(file_path)
            
            # Remove metadata
            if file_id in self.metadata:
                del self.metadata[file_id]
                self.save_metadata()
            
            # Log success
            transaction = {
                "timestamp": datetime.now().isoformat(),
                "user_id": user_id,
                "action": "DELETE",
                "file_id": file_id,
                "status": "SUCCESS"
            }
            self.blockchain.add_block(transaction)
            
            print(f"✓ File deleted: {file_id} by {user_id}")
            return True
        
        except FileNotFoundError:
            print(f"✗ File not found: {file_id}")
            return False
    
    def get_file_metadata(self, file_id: str) -> Optional[FileMetadata]:
        """Get metadata for a file"""
        return self.metadata.get(file_id)
    
    def list_files(self, user_id: str) -> List[str]:
        """List all files (shows only accessible files)"""
        return list(self.metadata.keys())
    
    def save_metadata(self):
        """Save metadata to file"""
        metadata_dict = {fid: meta.to_dict() for fid, meta in self.metadata.items()}
        with open('file_metadata.json', 'w') as f:
            json.dump(metadata_dict, f, indent=2)
    
    def load_metadata(self):
        """Load metadata from file"""
        try:
            with open('file_metadata.json', 'r') as f:
                metadata_dict = json.load(f)
            
            for file_id, meta_dict in metadata_dict.items():
                meta = FileMetadata(meta_dict['file_id'], meta_dict['owner_id'], 
                                   meta_dict['permissions'])
                meta.created = meta_dict['created']
                meta.last_modified = meta_dict['last_modified']
                self.metadata[file_id] = meta
        except FileNotFoundError:
            pass  # No existing metadata


# ============================================
# Demo
# ============================================

if __name__ == "__main__":
    """Demo file operations"""
    from blockchain import Blockchain
    
    print("\n" + "="*70)
    print("DEMO: File Operations with Blockchain Logging")
    print("="*70 + "\n")
    
    # Initialize
    bc = Blockchain()
    um = UserManager()
    fm = FileManager(bc, um)
    
    # Create files
    fm.create_file("test.txt", "admin001", "Hello World!")
    fm.create_file("data.txt", "user001", "User data")
    
    # Read file
    content = fm.read_file("test.txt", "admin001")
    print(f"Content: {content}")
    
    # Write to file
    fm.write_file("test.txt", "admin001", "Updated content")
    
    # Display blockchain
    bc.display_chain()

