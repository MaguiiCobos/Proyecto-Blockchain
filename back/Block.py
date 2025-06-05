import hashlib #We will use this library to create hashes

class Block:
    def __init__(self, index, timestamp, data, prior_hash=''):
        self.index = index # The position of the block in the chain
        self.timestamp = timestamp #The time when the block was created
        self.data = data #The actual transaction or data
        self.prior_hash = prior_hash #The hash of the previous block
        self.hash = '' #The hash of this block, which will be calculated later

    def crate_hash(self):
        # Convert all properties into a string and encode it
        block_string = f"{self.index}{self.timestamp}{self.data}{self.prior_hash}".encode()

        # Create a SHA-256 hash of the block string
        return hashlib.sha256(block_string).hexdigest()
    

class LunaBlockchain:
    def __init__(self): 
        # Initialize the chain with the genesis block
        self.chain = [self.create_genesis_block()] 

    def create_genesis_block(self):
        # Create the first block in the chain, known as the genesis block
        return Block(0, "2023-10-01", "ProbandoBlockchain", "0")

    def get_last_block(self):
        return self.chain[-1] # Get the last block in the chain
    
    def add_block(self, new_block):
        new_block.prior_hash = self.get_last_block().hash
        new_block.hash = new_block.crate_hash()
        self.chain.append(new_block)