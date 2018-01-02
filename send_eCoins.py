import ecdsa
import os
import sys
import binascii

hex_string_public_key = ""
hex_string_private_key = ""

with open('account.log', 'r') as file:
	lines = file.readlines()
	hex_string_private_key = lines[0][:-1]
	hex_string_public_key = lines[1][:-1]

#convert it into unicode characters
public_key = binascii.unhexlify(hex_string_public_key)
private_key = binascii.unhexlify(hex_string_private_key)

signing_key = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)

message = "{0}ECN{1}".format(sys.argv[2], sys.argv[1])
message_encoded = message.encode('utf-8')

signed_message = signing_key.sign(message_encoded)
print(signed_message)

command_string_args = "{0} {1} {2}".format(public_key, signed_message, message)

print(binascii.hexlify(signed_message))

print(command_string_args)

# command = "python3 communicate_to_miners.py " + command_string_args
# print("Loading transaction...")
# os.system(command)