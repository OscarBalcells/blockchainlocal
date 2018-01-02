import os
os.system("ifconfig en0 | egrep -o '([0-9]{1,3}\.){3}[0-9]{1,3}' | grep -v 255 > tmp")
with open('tmp', 'r') as file:
	#save the value in localhost
	localhost = file.readline() #only once

#delete the tmp file
os.system("rm tmp")
localhost = localhost[:-1]
print(localhost)
