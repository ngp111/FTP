from socket import *
import os
import pickle
from thread import * 

def show(conn) :
	filenameList = []
	for f in os.listdir(os.curdir) :
		filenameList.append(f)
	data = pickle.dumps(filenameList)
	conn.send(data)
	conn.close()

def trans(conn, cmd) :
	filename = cmd[3:]
	with open(filename) as f:
   		for line in f:
			if f == '' :
				break
			else :
				conn.send(line)
	print("data transmitted")
	#close(filename)
	conn.close()

def receive(conn, cmd) :
	filename = cmd[3:]
	fw = open(filename, "w")
	while True:
		file_lines = conn.recv(1024)
    		fw.write(file_lines)
    		if not file_lines:
        		print "file finished"
        		break;
	fw.close()
	conn.close()
	
def clientThread(conn, addr) :
	cmd = conn.recv(1024).decode()
	if cmd.upper() == 'LS' :
		show(conn)
	if cmd[:3].upper() == 'GET' :
		trans(conn, cmd)		
	if cmd[:3].upper() == 'PUT' :
		receive(conn, cmd)

serverport = 12000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverport))
serverSocket.listen(1)
print("Server is ready to receive")

list_of_clients = []

while True :
	conn, addr = serverSocket.accept()
	start_new_thread(clientThread, (conn, addr))









