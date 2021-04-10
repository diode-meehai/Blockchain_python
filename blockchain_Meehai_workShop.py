"""
Create a Blockchain by FutureSkill

To be installed:
    # Flask:pip install Flask
    # Postman HTTP Client: https://www.getpostman.com/

"""
import datetime
import hashlib
import json
from flask import Flask, jsonify


# Part 1 - Building a Blockchain

class Blockchain:

    def __init__(self):
        self.total_bill = 0
        self.chain = []
        self.create_block(proof=1, previous_hash='0')  # proof=Nonce

    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'total_bill': self.total_bill,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash}
        self.chain.append(block)
        return block

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):  # mine
        new_proof = 1
        check_proof = False
        while check_proof is False:
            # hexdigest แยกตัวอักษร แปลงเป็นเลขฐาน16
            hash_operation = hashlib.sha256(
                str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()  # สร้าง hash
            print('hash_operation > ' + str(new_proof) + ': ', hash_operation)
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):  # chain  -> Hash
        encoded_block = json.dumps(block, sort_keys=True).encode()  # เรียงลำดับตัวอังษร sort_keys
        print('encoded_block: ', encoded_block)
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True


# Creating a Web App
app = Flask(__name__)

Class_blockchain = Blockchain()


# Mining a new block
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = Class_blockchain.get_previous_block()
    previous_proof = previous_block['proof']

    proof = Class_blockchain.proof_of_work(previous_proof)  # Nonce

    previous_hash = Class_blockchain.hash(previous_block)
    print('previous_hash: ', previous_hash)

    block = Class_blockchain.create_block(proof, previous_hash)

    response = {'message': 'Congratulations, you just mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    return jsonify(response), 200


# Update total_bill
@app.route('/update_sell', methods=['GET'])
def update_sell():
    print('update_sell')
    Cost = 500000
    Class_blockchain.total_bill = Class_blockchain.total_bill + Cost  # บวกยอกใหม่

    previous_block = Class_blockchain.get_previous_block()
    previous_proof = previous_block['proof']

    proof = Class_blockchain.proof_of_work(previous_proof)  # Nonce

    previous_hash = Class_blockchain.hash(previous_block)
    print('previous_hash: ', previous_hash)

    block = Class_blockchain.create_block(proof, previous_hash)

    response = {'message': 'Congratulations, you just mined a block!',
                'Total sell': Class_blockchain.total_bill,
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}

    # print('response')
    return jsonify(response), 200


# Getting the full Blockchain
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {'chain': Class_blockchain.chain,
                'length': len(Class_blockchain.chain)}
    return jsonify(response), 200


# Homework Solution
# Checking if the Blockchain is valid
@app.route('/is_valid', methods=['GET'])
def is_valid():
    is_valid = Class_blockchain.is_chain_valid(Class_blockchain.chain)
    if is_valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'message': 'Houston, we have a problem. The Blockchain is not valid.'}
    return jsonify(response), 200


app.run(host='0.0.0.0', port=5100)

# Class_blockchain = Blockchain()
# Class_blockchain.create_block(proof=True,previous_hash='')
# print(Class_blockchain.hash(Class_blockchain.chain[0]))
# print(Class_blockchain.hash(Class_blockchain.chain[1]))

print(json.dumps({'key': 1}))

# Class_blockchain = Blockchain()
# print(block.chain)
# print('Genesis Block')
#
# print('------------\n 1nd Block')
# print(block.chain[0]['index'])
# print(block.chain[0]['timestamp'])
# print(block.chain[0]['proof'])
# print(block.chain[0]['previous_hash'])
#
# block.create_block(proof=1, previous_hash='Test')  # proof=Nonce
# print('------------\n 2nd Block')
# print(block.chain[1]['index'])
# print(block.chain[1]['timestamp'])
# print(block.chain[1]['proof'])
# print(block.chain[1]['previous_hash'])
