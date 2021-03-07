import base64

custom = "CDEFGHIJKLMNOPQRSTUVWXYZABcdefghijklmnopqrstuvwxyzab0123456789+/"
base = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

cipher = "BInaEi=="

string = ""

for c in cipher:
	if c in custom:
		string += base[custom.index(str(c))]
	elif c  == "=":
		string += "="

print(base64.b64decode(string))