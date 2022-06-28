from socket import *
import pickle

def show(conn) :
	conn.send(cmd.upper().encode())
	d_string = conn.recv(1024)
	data = pickle.loads(d_string)
	for f in data :
		print(f)
	conn.close()

def retrv(conn) :
	filename = raw_input('Enter filename to extract from server: ')
	cmd = 'get'+filename
	conn.send(cmd.encode())
	fw = open(filename, "w")
	while True:
		file_lines = clientSocket.recv(1024)
    		fw.write(file_lines)
    		if not file_lines:
        		print "file finished"
        		break;
	fw.close()
	conn.close()

def stor(conn) :
	filename = raw_input('Enter filename to store at server: ')
	cmd = 'put'+filename
	conn.send(cmd.encode())
	with open(filename) as f:
   		for line in f:
			if f == '' :
				break
			else :
				conn.send(line)
	print("data transmitted")
	#close(filename)
	conn.close()

servername = '192.168.43.202'
serverport = 12000

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((servername, serverport))
print("Connected to server")

print("Enter ls/get/put")

cmd = raw_input("Enter command: ")
if cmd.lower() == 'ls' :
	show(clientSocket)
elif cmd.lower() == 'get' :
	retrv(clientSocket)
elif cmd.lower() == 'put' :
	stor(clientSocket)
