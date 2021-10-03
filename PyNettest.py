"""
Script 01
Made by: Russell Dranch
"""
import os, subprocess, sys
from time import sleep

def system(cmd):
	command = subprocess.Popen([cmd], stdout = subprocess.PIPE, shell = True)
	return command.stdout.read()

def check_ping(ip):
	response = os.system("ping -c 5 " + ip + " 2>&1 >/dev/null")
	if response == 0:
		return True
	else:
		return False

def main():
	print "***STARTING TEST IN 3***"
	sleep(1)
	print("       2")
	sleep(.5)
	print("       1")
	sleep(.5)

	gateway = system("ip route | grep default").split(" ")
	
	if gateway == None:
		print "An error occured."
	else:	
		print "Default gateway: " + gateway[2]
	sleep(1)
	gw = gateway[2]
	gateway = check_ping(gw)
	if gateway:
		print "\nDefault gateway connection \033[42;42;42mSUCCESSFUL!\033[0;0;0m"
	else:
		print "\nDefault gateway connection \033[41;41;41mFAILED!\033[0;0;0m"
	sleep(1)
	getip = system("curl ifconfig.me")
	ip = check_ping(getip)

	if ip:
		print "\nRemote connection \033[42;42;42mSUCCESSFUL!\033[0;0;0m"
	else:
		print "\nRemote connection \033[41;41;41mFAILED!\033[0;0;0m"

	sleep(1)
	hn = system("hostname")
	hostname = check_ping(hn)

	if hostname:
		print "\nDNS resolution \033[42;42;42mSUCCESSFUL!\033[0;0;0m"
	else:
		print "\nDNS resolution \033[41;41;41mFAILED!\033[0;0;0m"
	

	print("\nTests Completed.")

main()
