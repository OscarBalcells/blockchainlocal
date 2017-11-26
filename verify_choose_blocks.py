import sys
import hashlib
#blockchains = sys.argv[1]
blockchains = []

miners_added = []

reconstructed_blockchains = []

#if we are miners we want to add our own blockchain too
with open('minerboolean', 'r') as file:
	if file.read()[:4] == "True":
		with open('blocks.csv', 'rw') as blocks:
			reconstructed_blockchains.append([])
			blockchain = blocks.readlines()
			reconstructed_blockchains[-1] = [block[:-1] for block in blockchain]

for i in range(len(blockchains)):
    blockchains[i] = str(blockchains[i])
    reconstructed_blockchains.append([])
    #we get the separate list of blocks
    reconstructed_blockchains[-1] = [blocks for blocks in blockchains[i].split('"\n", ')]
   


#we have to order the list from largest to shortest and verify until we find
# the largest legal block
reconstructed_blockchains.sort(key=len)
reconstructed_blockchains = reconstructed_blockchains[::-1]

breaking = False

index = 0
for blockchain in reconstructed_blockchains:
	for block in blockchain:
		reversed_block = block[::-1]
		hashable_block = block[:-reversed_block.index('[')-1]
		reversed_hashable_block = hashable_block[::-1]
		miner_add_in_block = hashable_block[-(reversed_hashable_block.index('[')):-1]
		if len(miner_add_in_block) > 0:
			miners_added.append([miner_add_in_block, index])
		final_hash = block[-(reversed_block.index('[')+1)+1:-1]
		if hashlib.sha256(hashable_block).hexdigest() == final_hash and final_hash[:4] == "0000":
			pass
		else:
			breaking = True
			#break
		#reconstructed_blockchains.remove(blockchain)
	index += 1

for miners_list in miners_added:
	if reconstructed_blockchains[0] == reconstructed_blockchains[miners_list[1]]:
		miners_list[0] = [miner for miner in miners_list[0].split(', ')]
		print("adding miners", miners_list[0])
		with open('miners_mac_addresses.log', 'a') as file:
			for miner in miners_list[0]:
				file.write(miner+" 1"+'\n')


if(len(reconstructed_blockchains) > 0):
	with open('blocks.csv', 'w') as file:
		for block in reconstructed_blockchains[0]:
			file.write(block)
			file.write('\n')

