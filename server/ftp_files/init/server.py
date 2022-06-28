from socket import *
import os
import pickle
from thread import * 

serverport = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverport))
serverSocket.listen(1)
print("Server is ready to receive")

list_of_clients = []

while True :
	connectionSocket, addr = serverSocket.accept()

	list_of_clients.append(connectionSocket)

	start_new_thread(clientThread, (connectionSocket, addr))

	cmd = connectionSocket.recv(1024).decode()
	if cmd == 'ls' :
		filenameList = []
		for f in os.listdir(os.curdir) :
			filenameList.append(f)
		data = pickle.dumps(filenameList)
		connectionSocket.send(data)
		connectionSocket.close()
	if cmd[0:3] == 'get':
		filename=cmd[3:]
		with open(filename) as f:
   			for line in f:
				if line == '':
					break
				else :
					connectionSocket.send(line)
		print("data transmitted")
		connectionSocket.close()
	if cmd[0:3] == 'put':
		filename=cmd[3:]
		fw = open("newfile.txt", "w")
		while True:
			file_lines = connectionSocket.recv(1024)
    			fw.write(file_lines)
    			if not file_lines:
        			print "file finished"
        			break;
		fw.close()
		connectionSocket.close()
serverSocket.close()

def clientThread(conn, addr) :
