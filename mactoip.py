import os

#open the miners log file and read the content
with open('miners_mac_addresses.log', 'r') as file:
	lines = file.readlines()
	lines = [line.strip() for line in lines]
	# we then store the data in two separate arrays
	mac_addresses = [item.split(' ')[0] for item in lines]
	trust_points = [int(item.split(' ')[1]) for item in lines]

#execute the command and read the output
os.system('arp -a > tmp')
command_output = open('tmp', 'r').read()
os.system('rm tmp')
#separate the output into an array of the lines
command_output = command_output.split('\n')

#find the ip address of each line in the output
#and store it in command_output_ip
#              and
#find the mac address of each line in the output
#and store it in command_output_mac
command_output_ip = []
command_output_mac = []
for command in command_output:
	try:
		command_output_ip.append(command[command.index('(')+1:command.index(')')])
		command_output_mac.append(command[command.index(')')+5:command.index(' on')])
	except Exception as e:
		pass

#erase the whole ipminers.log because it will be updated
open('miners_ip_addresses.log', 'w').close()

final_unorganized_ip_addresses = ["0" for i in range(len(trust_points))]

for i in range(len(command_output_ip)):
	try:
		index = mac_addresses.index(command_output_mac[i])		
		final_unorganized_ip_addresses[index] = command_output_ip[i]
	except ValueError:
		pass

final_organized_ip_addresses = []

def RecursiveCheckForIps():
	maximum_trusted = final_unorganized_ip_addresses[trust_points.index(max(trust_points))]
	if len(maximum_trusted) > 3:
		final_organized_ip_addresses.append(maximum_trusted)

	final_unorganized_ip_addresses.remove(maximum_trusted)
	trust_points.remove(max(trust_points))
	if len(final_unorganized_ip_addresses) > 0:
		RecursiveCheckForIps()

RecursiveCheckForIps()

print final_organized_ip_addresses

with open('miners_ip_addresses.log', 'w') as file:
	for i in final_organized_ip_addresses:
		file.write(i + '\n')







