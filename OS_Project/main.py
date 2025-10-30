"""
============================================
OS Project: Main Application
Blockchain-Based File Access Control System
============================================
Integrates all modules: Blockchain, File Manager, Access Control, Audit
"""

from blockchain import Blockchain
from file_manager import UserManager, FileManager
from access_control import AccessControl
from audit_reports import AuditReporter
import os
import sys

class FileAccessControlSystem:
    """Complete file access control system with blockchain"""
    
    def __init__(self):
        """Initialize all system components"""
        print("\n" + "="*70)
        print("BLOCKCHAIN-BASED FILE ACCESS CONTROL SYSTEM")
        print("="*70)
        print("\nInitializing system components...")
        
        # Initialize core modules
        self.blockchain = Blockchain()
        self.user_manager = UserManager()
        self.file_manager = FileManager(self.blockchain, self.user_manager)
        self.access_control = AccessControl(self.user_manager, self.file_manager, 
                                           self.blockchain)
        self.audit_reporter = AuditReporter(self.blockchain, self.user_manager)
        
        # Link access control to file manager
        self.file_manager.access_control = self.access_control
        
        print("✓ System initialized successfully\n")
        
        # Current logged-in user
        self.current_user = None
    
    def login(self, user_id: str):
        """Login a user"""
        user = self.user_manager.get_user(user_id)
        if user:
            self.current_user = user
            print(f"\n✓ Logged in as: {user.username} ({user.role})")
            return True
        else:
            print(f"\n✗ User not found: {user_id}")
            return False
    
    def logout(self):
        """Logout current user"""
        if self.current_user:
            print(f"\n✓ Logged out: {self.current_user.username}")
            self.current_user = None
        else:
            print("\n✗ No user logged in")
    
    def show_menu(self):
        """Display main menu"""
        print("\n" + "="*70)
        print("MAIN MENU")
        print("="*70)
        
        if self.current_user:
            print(f"\nLogged in as: {self.current_user.username} ({self.current_user.role})")
        else:
            print("\nNot logged in")
        
        print("\n1. Login")
        print("2. Create File")
        print("3. Read File")
        print("4. Write File")
        print("5. Delete File")
        print("6. List Files")
        print("7. View My Permissions")
        print("8. Generate Reports")
        print("9. View Blockchain")
        print("10. Validate Blockchain")
        print("11. Logout")
        print("0. Exit")
        print("="*70)
    
    def run(self):
        """Run the interactive system"""
        while True:
            self.show_menu()
            choice = input("\nEnter your choice: ").strip()
            
            if choice == '1':
                self.handle_login()
            elif choice == '2':
                self.handle_create_file()
            elif choice == '3':
                self.handle_read_file()
            elif choice == '4':
                self.handle_write_file()
            elif choice == '5':
                self.handle_delete_file()
            elif choice == '6':
                self.handle_list_files()
            elif choice == '7':
                self.handle_view_permissions()
            elif choice == '8':
                self.handle_reports()
            elif choice == '9':
                self.blockchain.display_chain()
            elif choice == '10':
                self.handle_validate_blockchain()
            elif choice == '11':
                self.logout()
            elif choice == '0':
                print("\n✓ Exiting system. Goodbye!")
                break
            else:
                print("\n✗ Invalid choice. Please try again.")
            
            input("\nPress Enter to continue...")
    
    def handle_login(self):
        """Handle user login"""
        print("\n" + "="*70)
        print("LOGIN")
        print("="*70)
        
        print("\nAvailable users:")
        for user_id, user in self.user_manager.users.items():
            print(f"  • {user_id}: {user.username} ({user.role})")
        
        user_id = input("\nEnter user ID: ").strip()
        self.login(user_id)
    
    def handle_create_file(self):
        """Handle file creation"""
        if not self.current_user:
            print("\n✗ Please login first")
            return
        
        print("\n" + "="*70)
        print("CREATE FILE")
        print("="*70)
        
        file_id = input("\nEnter file name: ").strip()
        content = input("Enter initial content (optional): ").strip()
        permissions = input("Permissions (private/public) [private]: ").strip() or 'private'
        
        self.file_manager.create_file(file_id, self.current_user.user_id, 
                                     content, permissions)
    
    def handle_read_file(self):
        """Handle file reading"""
        if not self.current_user:
            print("\n✗ Please login first")
            return
        
        print("\n" + "="*70)
        print("READ FILE")
        print("="*70)
        
        file_id = input("\nEnter file name: ").strip()
        content = self.file_manager.read_file(file_id, self.current_user.user_id)
        
        if content is not None:
            print(f"\n--- Content of {file_id} ---")
            print(content)
            print("---" + "-" * len(file_id) + "---")
    
    def handle_write_file(self):
        """Handle file writing"""
        if not self.current_user:
            print("\n✗ Please login first")
            return
        
        print("\n" + "="*70)
        print("WRITE FILE")
        print("="*70)
        
        file_id = input("\nEnter file name: ").strip()
        content = input("Enter new content: ").strip()
        
        self.file_manager.write_file(file_id, self.current_user.user_id, content)
    
    def handle_delete_file(self):
        """Handle file deletion"""
        if not self.current_user:
            print("\n✗ Please login first")
            return
        
        print("\n" + "="*70)
        print("DELETE FILE")
        print("="*70)
        
        file_id = input("\nEnter file name: ").strip()
        confirm = input(f"Are you sure you want to delete '{file_id}'? (yes/no): ").strip()
        
        if confirm.lower() == 'yes':
            self.file_manager.delete_file(file_id, self.current_user.user_id)
        else:
            print("\n✗ Deletion cancelled")
    
    def handle_list_files(self):
        """Handle file listing"""
        if not self.current_user:
            print("\n✗ Please login first")
            return
        
        print("\n" + "="*70)
        print("FILES IN SYSTEM")
        print("="*70)
        
        files = self.file_manager.list_files(self.current_user.user_id)
        
        if not files:
            print("\nNo files in system")
        else:
            print(f"\n{'File Name':<30} {'Owner':<15} {'Permissions':<10}")
            print("-" * 60)
            
            for file_id in files:
                meta = self.file_manager.get_file_metadata(file_id)
                if meta:
                    owner = self.user_manager.get_user(meta.owner_id)
                    owner_name = owner.username if owner else meta.owner_id
                    print(f"{file_id:<30} {owner_name:<15} {meta.permissions:<10}")
    
    def handle_view_permissions(self):
        """Handle viewing user permissions"""
        if not self.current_user:
            print("\n✗ Please login first")
            return
        
        summary = self.access_control.get_permission_summary(self.current_user.user_id)
        
        print("\n" + "="*70)
        print(f"YOUR PERMISSIONS: {summary['username']} ({summary['role']})")
        print("="*70)
        
        for action, perm in summary['permissions'].items():
            print(f"  {action}: {perm}")
    
    def handle_reports(self):
        """Handle report generation"""
        print("\n" + "="*70)
        print("AUDIT REPORTS")
        print("="*70)
        
        print("\n1. File Access Report")
        print("2. User Activity Report")
        print("3. Security Report (Unauthorized Attempts)")
        print("4. System Statistics")
        print("5. Export Blockchain to CSV")
        print("0. Back to Main Menu")
        
        choice = input("\nEnter your choice: ").strip()
        
        if choice == '1':
            file_id = input("\nEnter file name: ").strip()
            self.audit_reporter.generate_file_access_report(file_id)
        elif choice == '2':
            user_id = input("\nEnter user ID: ").strip()
            self.audit_reporter.generate_user_activity_report(user_id)
        elif choice == '3':
            self.audit_reporter.generate_security_report()
        elif choice == '4':
            self.audit_reporter.generate_summary_statistics()
        elif choice == '5':
            filename = input("\nEnter filename [blockchain_audit.csv]: ").strip()
            filename = filename or "blockchain_audit.csv"
            self.audit_reporter.export_blockchain_to_csv(filename)
        elif choice == '0':
            return
        else:
            print("\n✗ Invalid choice")
    
    def handle_validate_blockchain(self):
        """Handle blockchain validation"""
        print("\n" + "="*70)
        print("BLOCKCHAIN VALIDATION")
        print("="*70)
        
        print("\nValidating blockchain integrity...")
        is_valid = self.blockchain.validate_chain()
        
        if is_valid:
            print("✓ Blockchain is VALID - No tampering detected")
        else:
            print("✗ Blockchain is INVALID - Tampering detected!")
        
        print(f"\nTotal blocks: {self.blockchain.get_chain_length()}")


# ============================================
# Demo Function
# ============================================

def run_demo():
    """Run a pre-programmed demo"""
    print("\n" + "="*70)
    print("RUNNING AUTOMATED DEMO")
    print("="*70)
    
    system = FileAccessControlSystem()
    
    # Display permission matrix
    system.access_control.display_permission_matrix()
    
    # Demo scenarios
    print("\n" + "="*70)
    print("DEMO SCENARIO 1: Admin Operations")
    print("="*70)
    system.login("admin001")
    system.file_manager.create_file("admin_report.txt", "admin001", "Confidential data", "private")
    system.file_manager.create_file("public_notice.txt", "admin001", "Public announcement", "public")
    
    print("\n" + "="*70)
    print("DEMO SCENARIO 2: User Operations")
    print("="*70)
    system.login("user001")
    system.file_manager.create_file("my_notes.txt", "user001", "Personal notes", "private")
    system.file_manager.read_file("public_notice.txt", "user001")  # Should work
    system.file_manager.read_file("admin_report.txt", "user001")   # Should be denied
    
    print("\n" + "="*70)
    print("DEMO SCENARIO 3: Guest Operations")
    print("="*70)
    system.login("guest001")
    system.file_manager.read_file("public_notice.txt", "guest001")  # Should work
    system.file_manager.read_file("admin_report.txt", "guest001")   # Should be denied
    system.file_manager.delete_file("public_notice.txt", "guest001")  # Should be denied
    
    # Generate reports
    print("\n" + "="*70)
    print("GENERATING COMPREHENSIVE REPORTS")
    print("="*70)
    
    system.audit_reporter.generate_file_access_report("admin_report.txt")
    system.audit_reporter.generate_security_report()
    system.audit_reporter.generate_summary_statistics()
    
    # Display blockchain
    system.blockchain.display_chain()
    
    print("\n" + "="*70)
    print("DEMO COMPLETED SUCCESSFULLY")
    print("="*70)
    print("\nAll modules integrated and working:")
    print("  ✓ Student 1: Blockchain Core")
    print("  ✓ Student 2: File & User Management")
    print("  ✓ Student 3: Access Control")
    print("  ✓ Student 4: Audit & Reporting")
    print("="*70 + "\n")


# ============================================
# Main Entry Point
# ============================================

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--demo':
        # Run automated demo
        run_demo()
    else:
        # Run interactive system
        system = FileAccessControlSystem()
        system.run()

