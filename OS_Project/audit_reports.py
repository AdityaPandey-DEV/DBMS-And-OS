"""
============================================
OS Project: Audit & Reporting Module
Student 4: Blockchain Queries & Reports
============================================
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from blockchain import Blockchain, Block
from file_manager import UserManager
import json


class AuditReporter:
    """Generates audit reports from blockchain"""
    
    def __init__(self, blockchain: Blockchain, user_manager: UserManager):
        """
        Initialize audit reporter
        
        Args:
            blockchain: Blockchain instance to query
            user_manager: UserManager instance for user details
        """
        self.blockchain = blockchain
        self.user_manager = user_manager
    
    # ============================================
    # Query Functions
    # ============================================
    
    def query_file_access(self, file_id: str) -> List[Dict[str, Any]]:
        """
        Query all access attempts for a specific file
        
        Args:
            file_id: File to query
        
        Returns:
            List of transactions involving the file
        """
        results = []
        
        for block in self.blockchain.chain[1:]:  # Skip genesis block
            if isinstance(block.data, dict) and block.data.get('file_id') == file_id:
                results.append({
                    'block_index': block.index,
                    'timestamp': block.timestamp,
                    'user_id': block.data.get('user_id'),
                    'action': block.data.get('action'),
                    'status': block.data.get('status'),
                    'reason': block.data.get('reason', 'N/A')
                })
        
        return results
    
    def query_user_activity(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Query all actions performed by a specific user
        
        Args:
            user_id: User to query
        
        Returns:
            List of all user's transactions
        """
        results = []
        
        for block in self.blockchain.chain[1:]:
            if isinstance(block.data, dict) and block.data.get('user_id') == user_id:
                results.append({
                    'block_index': block.index,
                    'timestamp': block.timestamp,
                    'action': block.data.get('action'),
                    'file_id': block.data.get('file_id'),
                    'status': block.data.get('status')
                })
        
        return results
    
    def query_denied_access(self) -> List[Dict[str, Any]]:
        """
        Query all unauthorized access attempts (security violations)
        
        Returns:
            List of all denied transactions
        """
        results = []
        
        for block in self.blockchain.chain[1:]:
            if isinstance(block.data, dict) and block.data.get('status') == 'DENIED':
                results.append({
                    'block_index': block.index,
                    'timestamp': block.timestamp,
                    'user_id': block.data.get('user_id'),
                    'action': block.data.get('action'),
                    'file_id': block.data.get('file_id'),
                    'reason': block.data.get('reason', 'Unknown')
                })
        
        return results
    
    def query_timeline(self, start_time: str = None, end_time: str = None) -> List[Dict[str, Any]]:
        """
        Query operations within a time range
        
        Args:
            start_time: ISO format timestamp (optional)
            end_time: ISO format timestamp (optional)
        
        Returns:
            List of transactions in the time range
        """
        results = []
        
        for block in self.blockchain.chain[1:]:
            timestamp = block.timestamp
            
            # Check time range
            if start_time and timestamp < start_time:
                continue
            if end_time and timestamp > end_time:
                continue
            
            if isinstance(block.data, dict):
                results.append({
                    'block_index': block.index,
                    'timestamp': timestamp,
                    'user_id': block.data.get('user_id'),
                    'action': block.data.get('action'),
                    'file_id': block.data.get('file_id'),
                    'status': block.data.get('status')
                })
        
        return results
    
    def query_actions_by_type(self, action_type: str) -> List[Dict[str, Any]]:
        """
        Query all operations of a specific type
        
        Args:
            action_type: Action to filter (CREATE, READ, WRITE, DELETE)
        
        Returns:
            List of matching transactions
        """
        results = []
        
        for block in self.blockchain.chain[1:]:
            if isinstance(block.data, dict) and block.data.get('action') == action_type:
                results.append({
                    'block_index': block.index,
                    'timestamp': block.timestamp,
                    'user_id': block.data.get('user_id'),
                    'file_id': block.data.get('file_id'),
                    'status': block.data.get('status')
                })
        
        return results
    
    # ============================================
    # Report Generation Functions
    # ============================================
    
    def generate_file_access_report(self, file_id: str):
        """Generate formatted report for file access history"""
        print("\n" + "="*70)
        print(f"FILE ACCESS REPORT: {file_id}")
        print("="*70)
        
        results = self.query_file_access(file_id)
        
        if not results:
            print("No access records found for this file.")
            return
        
        print(f"\n{'Timestamp':<22} {'User':<15} {'Action':<10} {'Status':<10} {'Reason':<20}")
        print("-" * 90)
        
        for record in results:
            timestamp = record['timestamp'][:19]  # Truncate milliseconds
            user_id = record['user_id'] or 'N/A'
            action = record['action'] or 'N/A'
            status = record['status'] or 'N/A'
            reason = record['reason'] or '-'
            
            # Color code status
            status_display = f"✓ {status}" if status == "SUCCESS" else f"✗ {status}"
            
            print(f"{timestamp:<22} {user_id:<15} {action:<10} {status_display:<10} {reason:<20}")
        
        print("\n" + "="*70)
        print(f"Total Access Attempts: {len(results)}")
        print(f"Successful: {sum(1 for r in results if r['status'] == 'SUCCESS')}")
        print(f"Denied: {sum(1 for r in results if r['status'] == 'DENIED')}")
        print("="*70 + "\n")
    
    def generate_user_activity_report(self, user_id: str):
        """Generate formatted report for user activity"""
        user = self.user_manager.get_user(user_id)
        username = user.username if user else user_id
        
        print("\n" + "="*70)
        print(f"USER ACTIVITY REPORT: {username} ({user_id})")
        print("="*70)
        
        results = self.query_user_activity(user_id)
        
        if not results:
            print("No activity found for this user.")
            return
        
        print(f"\n{'Timestamp':<22} {'Action':<10} {'File':<20} {'Status':<10}")
        print("-" * 70)
        
        for record in results:
            timestamp = record['timestamp'][:19]
            action = record['action'] or 'N/A'
            file_id = record['file_id'] or 'N/A'
            status = record['status'] or 'N/A'
            
            status_display = f"✓ {status}" if status == "SUCCESS" else f"✗ {status}"
            
            print(f"{timestamp:<22} {action:<10} {file_id:<20} {status_display:<10}")
        
        print("\n" + "="*70)
        print(f"Total Actions: {len(results)}")
        print(f"Successful: {sum(1 for r in results if r['status'] == 'SUCCESS')}")
        print(f"Denied: {sum(1 for r in results if r['status'] == 'DENIED')}")
        print("="*70 + "\n")
    
    def generate_security_report(self):
        """Generate security audit report (unauthorized access attempts)"""
        print("\n" + "="*70)
        print("SECURITY AUDIT REPORT - Unauthorized Access Attempts")
        print("="*70)
        
        results = self.query_denied_access()
        
        if not results:
            print("\n✓ No unauthorized access attempts detected. System is secure.")
            print("="*70 + "\n")
            return
        
        print(f"\n{'Timestamp':<22} {'User':<15} {'Action':<10} {'File':<20} {'Reason':<25}")
        print("-" * 95)
        
        for record in results:
            timestamp = record['timestamp'][:19]
            user_id = record['user_id'] or 'N/A'
            action = record['action'] or 'N/A'
            file_id = record['file_id'] or 'N/A'
            reason = record['reason'][:24]  # Truncate long reasons
            
            print(f"{timestamp:<22} {user_id:<15} {action:<10} {file_id:<20} {reason:<25}")
        
        # Aggregate statistics
        users_with_violations = {}
        for record in results:
            user_id = record['user_id']
            users_with_violations[user_id] = users_with_violations.get(user_id, 0) + 1
        
        print("\n" + "="*70)
        print(f"Total Unauthorized Attempts: {len(results)}")
        print("\nTop Violators:")
        sorted_violators = sorted(users_with_violations.items(), key=lambda x: x[1], reverse=True)
        for user_id, count in sorted_violators[:5]:
            user = self.user_manager.get_user(user_id)
            username = user.username if user else user_id
            print(f"  • {username} ({user_id}): {count} violations")
        
        print("\n⚠ RECOMMENDATION: Investigate users with multiple violations")
        print("="*70 + "\n")
    
    def generate_summary_statistics(self):
        """Generate overall system statistics"""
        print("\n" + "="*70)
        print("SYSTEM STATISTICS SUMMARY")
        print("="*70)
        
        total_blocks = self.blockchain.get_chain_length() - 1  # Exclude genesis
        
        # Count by action type
        action_counts = {'CREATE': 0, 'READ': 0, 'WRITE': 0, 'DELETE': 0}
        status_counts = {'SUCCESS': 0, 'DENIED': 0, 'FAILED': 0}
        
        for block in self.blockchain.chain[1:]:
            if isinstance(block.data, dict):
                action = block.data.get('action')
                status = block.data.get('status')
                
                if action in action_counts:
                    action_counts[action] += 1
                if status in status_counts:
                    status_counts[status] += 1
        
        print(f"\nTotal Transactions: {total_blocks}")
        print(f"Blockchain Length: {self.blockchain.get_chain_length()} blocks")
        print(f"Chain Valid: {'✓ YES' if self.blockchain.validate_chain() else '✗ NO'}")
        
        print("\nOperations by Type:")
        for action, count in action_counts.items():
            print(f"  • {action}: {count}")
        
        print("\nOperations by Status:")
        for status, count in status_counts.items():
            if count > 0:
                percentage = (count / total_blocks * 100) if total_blocks > 0 else 0
                print(f"  • {status}: {count} ({percentage:.1f}%)")
        
        # Security metrics
        security_rate = (status_counts['SUCCESS'] / total_blocks * 100) if total_blocks > 0 else 100
        print(f"\n Security Success Rate: {security_rate:.1f}%")
        
        print("="*70 + "\n")
    
    # ============================================
    # Export Functions
    # ============================================
    
    def export_report_to_json(self, report_type: str, filename: str, **kwargs):
        """Export report to JSON file"""
        if report_type == 'file_access':
            data = self.query_file_access(kwargs.get('file_id'))
        elif report_type == 'user_activity':
            data = self.query_user_activity(kwargs.get('user_id'))
        elif report_type == 'security':
            data = self.query_denied_access()
        elif report_type == 'timeline':
            data = self.query_timeline(kwargs.get('start_time'), kwargs.get('end_time'))
        else:
            print(f"Unknown report type: {report_type}")
            return
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✓ Report exported to {filename}")
    
    def export_blockchain_to_csv(self, filename: str = "blockchain_audit.csv"):
        """Export entire blockchain to CSV"""
        import csv
        
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Block', 'Timestamp', 'User', 'Action', 'File', 'Status', 'Hash'])
            
            for block in self.blockchain.chain[1:]:
                if isinstance(block.data, dict):
                    writer.writerow([
                        block.index,
                        block.timestamp,
                        block.data.get('user_id', 'N/A'),
                        block.data.get('action', 'N/A'),
                        block.data.get('file_id', 'N/A'),
                        block.data.get('status', 'N/A'),
                        block.hash[:16] + '...'
                    ])
        
        print(f"✓ Blockchain exported to {filename}")


# ============================================
# Demo
# ============================================

if __name__ == "__main__":
    """Demo audit and reporting"""
    from blockchain import Blockchain
    from file_manager import UserManager, FileManager
    from access_control import AccessControl
    
    print("\n" + "="*70)
    print("DEMO: Audit & Reporting System")
    print("="*70 + "\n")
    
    # Initialize system
    bc = Blockchain()
    um = UserManager()
    fm = FileManager(bc, um)
    ac = AccessControl(um, fm, bc)
    fm.access_control = ac
    
    # Create audit reporter
    reporter = AuditReporter(bc, um)
    
    # Simulate some operations
    print("Simulating file operations...\n")
    fm.create_file("report.txt", "admin001", "Quarterly report")
    fm.read_file("report.txt", "admin001")
    fm.read_file("report.txt", "user001")  # Should be denied (private)
    fm.create_file("public.txt", "admin001", "Public data", "public")
    fm.read_file("public.txt", "guest001")  # Should succeed (public)
    fm.delete_file("public.txt", "guest001")  # Should be denied
    fm.write_file("report.txt", "admin001", "Updated report")
    
    # Generate reports
    print("\n" + "="*70)
    print("GENERATING AUDIT REPORTS")
    print("="*70)
    
    # Report 1: File access history
    reporter.generate_file_access_report("report.txt")
    
    # Report 2: User activity
    reporter.generate_user_activity_report("guest001")
    
    # Report 3: Security violations
    reporter.generate_security_report()
    
    # Report 4: System statistics
    reporter.generate_summary_statistics()
    
    # Export reports
    print("\nExporting reports...")
    reporter.export_report_to_json('security', 'security_report.json')
    reporter.export_blockchain_to_csv('blockchain_audit.csv')
    
    # Display blockchain
    bc.display_chain()

