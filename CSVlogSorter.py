"""
By Russell Dranch
Script O4
Log file stuff
"""

#Basic python imports
from geoip import geolite2
import csv, os, sys
import win_inet_pton
 
#Gets the filename the user input
file = sys.argv[1]
print "File name is " + file
 
#Checks to see if a file was input. Will quit if nothing was input.
if file == None or file == " ":
	print "> Error. Could not open file or file not provided."
	exit(1)

#Attempts to open the file. Prints an error and quits if the file was not found
try:
	f = open(file)
	f.close()
except NameError:
	print "> Error. Could not open file or file not provided."
	exit(1)
except IOError:
	print "> Error. Could not open file or file not provided."
	exit(1)


#Gets user input to name the file
userInput = raw_input("Give me a new file name: ")
	
"""
Function to check if a string is a valid ip. Takes a string as a param
and returns a boolean.
"""
def check_ip(ip):
	splitter = ip.split(".")
	if len(splitter) != 4:
		return False
	for num in splitter:
		if not num.isdigit():
			return False
		if int(num) < 0 or int(num) > 255:
			return False
	return True
 
d = dict()
 
#Creates a dictionary that adds all ips addresses and the times they appear
with open(file, 'r') as f:
	for line in f:
		x = line.split(" ")
		
		for index in x:
			if check_ip(index):
				if (index not in d.keys()):
					d[index] = 1
				else:
					d[index] += 1

print "Count\tIP\tLocation"
z = 0
"""
Creates a .CSV file and prints/inputs the country, its ip,
and the times that ip appeared if its over 10 to the console and .CSV file
"""
with open(userInput + ".csv", 'w') as new_file:
	for elements in d:
		csv_file = csv.writer(new_file, delimiter=',',quotechar='"', quoting=csv.QUOTE_MINIMAL)
		
		try:
			location = geolite2.lookup(elements).country
		except AttributeError:
			location = "N/A"
		
		#print "Location: " + location
		if d[elements] <= 10:
			continue
		if z == 0:
			csv_file.writerow(["Count", "IP", "Location"])
			z += 1
		csv_file.writerow([d[elements], elements, location])
		print str(d[elements]) + "\t" + str(elements) + "\t" +  location
					
