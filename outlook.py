import csv, os, sys, subprocess, extract_msg, win32com.client

print("[*] Place me into the Logs folder then continue the script. [Enter]")
input()

#Reads all .txt files in the current dir
files = filter(lambda x: x[-4:] == ".msg" and len(x) > 4, os.listdir())
ol = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")


if files == None:
	print ("> No files input. Quitting.")
	exit(1)

def attachsave(filename):
	att = ol.OpenSharedItem(filename).Attachments.Item(1).SaveAsFile(os.getcwd() + "\\" + "att.msg")

def msgparse(body):
	lst = [pos for pos, char in enumerate(body) if char == '"']

	try:
		subject = body[lst[0]+1:lst[1]]
	except:
		subject = " "
	try:
		sender = body[lst[2]+1:lst[3]]
	except:
		sender = " "
	try:
		recipient = body[lst[4]+1:lst[5]]
	except:
		recipient = " "
	return [subject, sender, recipient]

#The name of the .csv file to create. Name whatever
userInput = "viplog2019NEW"

#print ("Subject\Sender\Recipient")
"""
Creates a .CSV file. Extracts information from parser and places them into respective line
"""
with open(userInput + ".csv", 'w', encoding="utf-8") as new_file:
	print("> Creating CVS file. This might take some time depending on the log files.")

	csv_file = csv.writer(new_file, delimiter=',', lineterminator="\n", quotechar='"', quoting=csv.QUOTE_MINIMAL)
	csv_file.writerow(["Subject", "Sender", "Recipient"])
	
	for file in files:
		filename = os.getcwd() + "\\" + file
		attachsave(filename)
		f = r'att.msg'
		msg = extract_msg.Message(f)
		if msg.sender[0] == "=":
			msg_sender = msg.sender[30:]
		else:
			msg_sender = msg.sender
		msg_subject = msg.subject
		if msg.cc != " " and msg.cc is not None and msg.to is not None:
			msg_recipient = msg.to + ", " + msg.cc
		else:
			msg_recipient = msg.to
		csv_file.writerow([msg_subject, msg_sender, msg_recipient])

os.sleep(3)
os.remove(os.getcwd()+"\\"+"att.msg")
print("> Completed. Check your folder.")
