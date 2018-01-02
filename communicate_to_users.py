import sys
import socket
import threading
import socket
import sys
import threading
import random

def add_new_miner(mac_address):
	# we add a new miner for implementing it into the 
	# next block we mine
	with open('new_miners.log', 'a') as file:
		mac_addr = mac.decode('utf-8')
		file.write(mac_addr+'\n')

def add_new_transaction(transaction):
	#add new transaction to our pending transactions list
	#we first check the balance and in case it has the
	#the necessary amount for doing the transaction, it
	#will be executed
	address_balance = 0

	transaction_parts = [splitted_part for splitted_part in transaction.split(', ')]
	#the transaction address of the sender is the first element in the string list
	tx_address = transaction_parts[0][1:]
	#the amount it sends
	tx_amount = transaction_parts[2][:transaction_parts[2].index('E')]

	with open('blocks.csv', 'r') as file:
		#read all the blocks in our database to check for the sender balance
		blocks = file.readlines()
	for block in blocks:
		if tx_address in block:
			#findind out if the address has mined any block
			char1 = [pos for pos, char in enumerate(block) if char == "["][3]-1
			char2 = [pos for pos, char in enumerate(block) if char == "]"][3]
			miner = block[char1:char2]
			if tx_address == miner:
				address_balance += 50
			#very complicated process for finding the 
			#block of transactions in the block
			if "[]" in block:
				index_end_tx = block.index("[]")
			else:	
				index_end_tx = block.index(':') - 4
			if block[idex_end_tx] != "]":
				index_end_tx += 1

			index_str_tx = block.index("[[") + 2

			transaction_block = block[index_str_tx:index_end_tx].split('], ')


			for transaction in transaction_block:
				if tx_address in transaction:
					transaction_process = [s for s in transaction.split(', ')]
					quantity = int(transaction_process[2][:transaction_process[2].index('E')])
					if tx_address in transaction_process[0] and tx_address in transaction_process[2]:
						#if the address sends funds to itself nothing happens
						pass
					elif public_address in transaction_process[0]:
						balance -= quantity
					elif public_address in transaction_process[2]:
						balance += quantity
	if address_balance >= tx_amount:
		with open('new_transactions.log', 'a') as file:
			transaction = transaction.decode('utf-8')
			file.write(transaction+'\n')

def send_my_blocks():
	with open('blocks.csv', 'r') as file:
		lines = file.readlines()
		blocks = [line[:-1] for line in lines]

	#convert list into a string we can encode and send
	blocks_string = "["
	for block_index in range(len(blocks)):
		blocks_string += blocks[block_index]
		if block_index < len(blocks) - 1:
			blocks_string += ", "
	blocks_string += "]"

	return blocks_string


class Server:
	def __init__(self):
		self.connections = []
		self.peers = []
		self.identification = 0
		self.connection_closed = False

		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM,)
		sock.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		sock.bind(('0.0.0.0', 10000))
		sock.listen(1)

		while True:
			conn, addr = sock.accept()
			chThread = threading.Thread(target=self.handler,args=(conn, str(addr[0]), self.identification))
			chThread.start()
			self.connections.append([conn, self.identification])
			self.identification += 1
			blockchain_message = send_my_blocks()
			for [connection, _] in self.connections:
				connection.sendall(blockchain_message)
			self.connection_closed = True

	def handler(self, connection, address, identif):
		# sends a welcome message to the new participant

		data = connection.recv(2048)
		message = data.decode('utf-8')

		if [connection, identif] in self.connections:
			self.connections.remove([connection, identif])
		if len(message) < 1:
			print("Data not received")
		elif message[0] == '\t':
			print("No transaction")
		elif message[0] == '\a':
			print("New miner added")
			add_new_miner(message[1:])
		else:
			print("Transaction: ", message)
			add_new_transaction(message)
		while self.connection_closed == False:
			pass
		connection.close()

server = Server()


