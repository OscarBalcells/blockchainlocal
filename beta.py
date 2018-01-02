import hashlib
hashable_block = "0,0000000000,0,[[xxx,100,588d202afcc1ee4ab5254c7847ec25b9a135bbda0f2bc69ee1a714749fd77dc9f88ff2a00d7e752]],,"
hashable_block = hashable_block.encode('utf-8')
final_hash = hashlib.sha256(hashable_block).hexdigest()
print(final_hash)