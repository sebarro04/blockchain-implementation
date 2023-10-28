import hashlib
import json
import time

class Block:
    def __init__(self, index, previous_hash, timestamp, transactions, proof):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = timestamp
        self.transactions = transactions
        self.proof = proof
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "0", "Genesis Block", 0, 0)  # Genesis block has no previous hash

    def add_block(self, block):
        block.previous_hash = self.chain[-1].hash
        self.chain.append(block)

    def is_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True
    
    def mine_block(self, proof_prefix):
        while True:
            new_proof = self.proof_of_work()
            if new_proof[:len(proof_prefix)] == proof_prefix:
                break

        new_block = Block(len(self.chain), self.chain[-1].hash, time.time(), "New Transactions", new_proof)
        self.add_block(new_block)

    def proof_of_work(self):
        proof = 0
        while self.is_valid_proof(proof) is False:
            proof += 1
        return str(proof)

    @staticmethod
    def is_valid_proof(proof):
        return hashlib.sha256(str(proof).encode()).hexdigest()[:4] == "0000"
    
if __name__ == '__main__':
    blockchain = Blockchain()
    proof_prefix = "0000"  # Adjust this based on the desired level of difficulty

    for _ in range(5):
        blockchain.mine_block(proof_prefix)

    for block in blockchain.chain:
        print(f"Block {block.index}: {block.hash}")
