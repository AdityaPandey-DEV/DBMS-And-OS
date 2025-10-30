"""
============================================
OS Project: Blockchain Core Module
Student 1: Blockchain Implementation
============================================
"""

import hashlib
import json
from datetime import datetime
from typing import List, Dict, Any

class Block:
    """Represents a single block in the blockchain"""
    
    def __init__(self, index: int, timestamp: str, data: Dict[str, Any], 
                 previous_hash: str, hash: str = None):
        """
        Initialize a block
        
        Args:
            index: Position in the blockchain
            timestamp: When the block was created
            data: Transaction data (file operation details)
            previous_hash: Hash of the previous block
            hash: Hash of this block (calculated if not provided)
        """
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = hash or self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """
        Calculate SHA256 hash of the block
        
        Returns:
            64-character hexadecimal hash string
        """
        # Create string representation of block data
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash
        }, sort_keys=True)
        
        # Calculate SHA256 hash
        return hashlib.sha256(block_string.encode()).hexdigest()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert block to dictionary for serialization"""
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "hash": self.hash
        }
    
    def __repr__(self) -> str:
        """String representation of block"""
        return f"Block(index={self.index}, hash={self.hash[:16]}...)"


class Blockchain:
    """Manages the blockchain"""
    
    def __init__(self):
        """Initialize blockchain with genesis block"""
        self.chain: List[Block] = []
        self.create_genesis_block()
    
    def create_genesis_block(self):
        """Create the first block in the blockchain"""
        genesis_block = Block(
            index=0,
            timestamp=datetime.now().isoformat(),
            data={"message": "Genesis Block - Blockchain Initialized"},
            previous_hash="0"
        )
        self.chain.append(genesis_block)
        print(f"✓ Genesis block created: {genesis_block.hash[:16]}...")
    
    def get_latest_block(self) -> Block:
        """Get the most recent block in the chain"""
        return self.chain[-1]
    
    def add_block(self, data: Dict[str, Any]) -> Block:
        """
        Add a new block to the blockchain
        
        Args:
            data: Transaction data to store in the block
            
        Returns:
            The newly created block
        """
        previous_block = self.get_latest_block()
        new_block = Block(
            index=len(self.chain),
            timestamp=datetime.now().isoformat(),
            data=data,
            previous_hash=previous_block.hash
        )
        self.chain.append(new_block)
        return new_block
    
    def validate_chain(self) -> bool:
        """
        Validate the integrity of the blockchain
        
        Returns:
            True if blockchain is valid, False if tampered
        """
        # Genesis block is always valid
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            
            # Check 1: Is the current block's hash correct?
            if current_block.hash != current_block.calculate_hash():
                print(f"✗ Invalid hash at block {i}")
                print(f"  Stored hash:     {current_block.hash}")
                print(f"  Calculated hash: {current_block.calculate_hash()}")
                return False
            
            # Check 2: Does the current block properly link to previous block?
            if current_block.previous_hash != previous_block.hash:
                print(f"✗ Broken chain link at block {i}")
                print(f"  Current block's previous_hash: {current_block.previous_hash}")
                print(f"  Previous block's hash:         {previous_block.hash}")
                return False
        
        return True
    
    def get_chain_length(self) -> int:
        """Get the number of blocks in the chain"""
        return len(self.chain)
    
    def get_block(self, index: int) -> Block:
        """Get a block by index"""
        if 0 <= index < len(self.chain):
            return self.chain[index]
        return None
    
    def display_chain(self):
        """Display the entire blockchain in a readable format"""
        print("\n" + "="*70)
        print("BLOCKCHAIN VISUALIZATION")
        print("="*70)
        
        for block in self.chain:
            print(f"\nBlock {block.index}")
            print(f"├─ Timestamp: {block.timestamp}")
            print(f"├─ Hash:      {block.hash}")
            print(f"├─ Prev Hash: {block.previous_hash}")
            print(f"└─ Data:      {json.dumps(block.data, indent=11)[11:]}")
            
            if block.index < len(self.chain) - 1:
                print("       ↓")
        
        print("\n" + "="*70)
        print(f"Total Blocks: {len(self.chain)}")
        print(f"Chain Valid: {'✓ YES' if self.validate_chain() else '✗ NO'}")
        print("="*70 + "\n")
    
    def save_to_file(self, filename: str = "blockchain.json"):
        """Save blockchain to JSON file"""
        chain_data = [block.to_dict() for block in self.chain]
        with open(filename, 'w') as f:
            json.dump(chain_data, f, indent=2)
        print(f"✓ Blockchain saved to {filename}")
    
    def load_from_file(self, filename: str = "blockchain.json"):
        """Load blockchain from JSON file"""
        try:
            with open(filename, 'r') as f:
                chain_data = json.load(f)
            
            self.chain = []
            for block_data in chain_data:
                block = Block(
                    index=block_data['index'],
                    timestamp=block_data['timestamp'],
                    data=block_data['data'],
                    previous_hash=block_data['previous_hash'],
                    hash=block_data['hash']
                )
                self.chain.append(block)
            
            print(f"✓ Blockchain loaded from {filename}")
            print(f"  Loaded {len(self.chain)} blocks")
            
            # Validate loaded chain
            if self.validate_chain():
                print("  ✓ Blockchain integrity verified")
            else:
                print("  ✗ Warning: Blockchain integrity check failed!")
        
        except FileNotFoundError:
            print(f"✗ File {filename} not found")
        except json.JSONDecodeError:
            print(f"✗ Invalid JSON in {filename}")


# ============================================
# Demo & Testing Functions
# ============================================

def demo_basic_blockchain():
    """Demonstrate basic blockchain functionality"""
    print("\n" + "="*70)
    print("DEMO: Basic Blockchain Operations")
    print("="*70)
    
    # Create blockchain
    bc = Blockchain()
    
    # Add some blocks
    bc.add_block({"user": "admin001", "action": "CREATE", "file": "file1.txt", "status": "SUCCESS"})
    bc.add_block({"user": "user002", "action": "READ", "file": "file1.txt", "status": "SUCCESS"})
    bc.add_block({"user": "guest001", "action": "DELETE", "file": "file1.txt", "status": "DENIED"})
    
    # Display blockchain
    bc.display_chain()
    
    return bc


def demo_tampering_detection():
    """Demonstrate tamper detection"""
    print("\n" + "="*70)
    print("DEMO: Tampering Detection")
    print("="*70)
    
    # Create blockchain
    bc = Blockchain()
    bc.add_block({"user": "admin001", "action": "CREATE", "file": "passwords.txt"})
    bc.add_block({"user": "user002", "action": "READ", "file": "passwords.txt"})
    
    print("\n1. Original blockchain:")
    print(f"   Block 1 data: {bc.chain[1].data}")
    print(f"   Validation: {'✓ VALID' if bc.validate_chain() else '✗ INVALID'}")
    
    # Tamper with block 1
    print("\n2. Tampering with Block 1 data...")
    print("   Changing user 'admin001' → 'hacker999'")
    bc.chain[1].data['user'] = 'hacker999'
    
    print("\n3. After tampering:")
    print(f"   Block 1 data: {bc.chain[1].data}")
    print(f"   Validation: {'✓ VALID' if bc.validate_chain() else '✗ INVALID'}")
    
    print("\n✓ Tampering detected! Blockchain immutability proven.\n")


if __name__ == "__main__":
    """Run demos when executed directly"""
    
    # Demo 1: Basic operations
    blockchain = demo_basic_blockchain()
    
    # Demo 2: Tampering detection
    demo_tampering_detection()
    
    # Save blockchain
    blockchain.save_to_file("blockchain_demo.json")

