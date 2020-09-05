''' 
Script - Russell Dranch
Log parser
'''
#Something that would speed up the script is having the API check for Amazon services instead of
#downloading it off Powershell then checking through all of them as that's very time consuming.
#This wasn't done in order to not use too many free keys.

from geoip import geolite2
import csv, os, sys, subprocess, ipaddress
from networksdb import NetworksDB

#NetworksDB API key - free
api = NetworksDB('')
#INPUT KEY HERE


print("[*] Place me into the Logs folder then continue the script. [Enter]")
input()

#Reads all .txt files in the current dir
files = filter(lambda x: x[-4:] == ".txt" and len(x) > 4, os.listdir())

if files == None:
	print ("> No files input. Quitting.")
	exit(1)

#Creates a local file listing the IPs of all of Amazons servers and appends that into a list
print("> Creating list of Amazon webservices...")
p = subprocess.call(['powershell.exe', 'Get-AWSPublicIpAddressRange -ServiceKey AMAZON | where {$_.IpAddressFormat -eq "Ipv4"} | select IpPrefix | Out-File amazon.txt -Encoding utf8'], stdout=sys.stdout)
lst = []
with open('amazon.txt', 'r') as aws:
	for l in aws:
		l = l.strip("\n  ï»¿")
		lst.append(l)
print("> Done.")


#The name of the .csv file to create. Name whatever
userInput = "combolog_new"
	
"""
Function to check if a string is a valid ip. Takes a string as a param
and returns a boolean. Inefficient should be using IPAddress.
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
 
"""
Determines if an IP is from <redacted>, Amazon or neither
Returns 0 if from neither, 1 if from Amazon and 2 from <redacted>
"""
def isWhat(ip):	
	if (ip[0:7] == "<redacted>"):
		return 2

	for ips in lst:
		if (ip[0:3] != ips[0:3]):
			continue
		try:
			if (ipaddress.IPv4Address(ip) in ipaddress.IPv4Network(ips)):
				return 1
		except ValueError:
			continue
	else:
		return 0
	

#Creates a dictionary that adds all IP addresses and the times they appear
for file_sep in files:
	with open(file_sep, 'r') as f:
		for line in f:
			x = line.split(" ")
			
			for index in x:
				if check_ip(index):
					if (index not in d.keys()):
						d[index] = 1
					else:
						d[index] += 1



#print ("Count\tIP\tLocation\tType")
z = 0
"""
Creates a .CSV file and prints/inputs the country, its IP,
the times that IP appeared, where it's from and a .CSV file
"""
with open(userInput + ".csv", 'w') as new_file:
	print("> Creating CVS file. This might take some time depending on the log files.")
	typ = "None"

	for elements in d:
		csv_file = csv.writer(new_file, delimiter=',', lineterminator="\n", quotechar='"', quoting=csv.QUOTE_MINIMAL)
		
		try:
			location = geolite2.lookup(elements).country
		except AttributeError:
			location = "N/A"

		if (ipaddress.ip_address(elements).is_private == True):
			typ = "Private"
		elif (isWhat(elements) == 1):
			typ = "Amazon"
		elif (isWhat(elements) == 2):
			typ = "<redacted>"
		elif (isWhat(elements) == 0):
			#Based on DatabaseDB module
			try:
				ip_org = api.ip_info(elements)
				typ = ip_org.organisation.name
			except Exception:
				typ = 'External'
			#----------------------------#
		else:
			typ = "?"

		if z == 0:
			csv_file.writerow(["Count", "IP", "Location", "Type"])
			z += 1
		csv_file.writerow([d[elements], elements, location, typ])
print("> Completed. Check your folder.")