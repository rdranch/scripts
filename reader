import csv, os


"""
Reader function. Takes a file and parses it into different values
"""
def reader(file, mod):
	with open(file, mode=str(mod)) as csvf:
		reader = csv.DictReader(csvf)
		users = set()
		groups = set()
		
		for row in reader:
			user = ""
			first = ""
			last = ""
			fname = ""
			EID = ""
			group = ""
			directory = ""
			dep = ""
			
			EID = row['EmployeeID']
			if len(EID) == 0:
				print "> EID not found"			
				continue

			last = row['LastName']
			if len(last) == 0:
				print "> lname not found"
				continue				

			first = str(row['FirstName']) #Possible error?
			if len(first) == 0:
				print "> fname not found"
				continue
			
			dep = row['Department']
			if len(dep) == 0:
				print "> Department not found"
				continue
			
			group = row['Group']
			if group in groups:
				pass
				#print group + " exists"
			else:
				groups.add(group)
				os.system("groupadd " + group)

			fname = str(first) + " " + str(last)

			lname = "".join(list([val for val in last if val.isalpha()]))
					
			user = first[0].lower() + lname.lower()

			if user in users:
				x = 0
				for val in users:
					if val.strip('0123456789') == user:
						x += 1
				user += str(x)
				users.add(user)
			else:
				users.add(user)
			
			directory = "/home/" + dep + "/" + user + "/"
			#print "THE DIRECTORY IS: " + directory
			add_user = "useradd -m -d " + directory + " -u " + EID + " -g " + group + " -s /bin/csh -p " + "password" + " " + user 
			print add_user			
			os.system(add_user)
			#os.system("passwd -f " + user)
			print "chage -d0 " + user
			print "Expiring passwd for " + user
			os.system("chage -d0 " + user)


file = "/home/student/Desktop/Lab02_Users.csv"
print "> Missing information will not be recorded."
reader(file, 'r')
