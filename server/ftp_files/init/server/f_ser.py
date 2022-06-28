from socket import *
import threading
import os
import pickle

command_port = 12000
data_port = command_port - 1

class ftp_server() :
	def __init__(self) :
		self.command_port = 12000
		self.serverSocket = socket(AF_INET, SOCK_STREAM)
		self.serverSocket.bind(('', self.serverport))
		
		self.serverSocket.listen(1)
		print('Server is listening')
		while True :
			conn, addr = self.serverSocket.accept()
			cmd_thread = spawn_thread(conn)
			cmd_thread.start()

class spawn_thread(threading.Thread) :
	def __init__(self, conn) :
		self.conn = conn
		self.curr_dir = '/home/hp/init/server/ftp-files'
		threading.Thread.__init__(self)
		self.running_status = True
	
	def run(self) :
		while True :
			cmd = self.conn.recv(1024).decode()
			if cmd.upper() == 'OPEN' :
				self.show()

	

if __name__ == '__main__' :
	server = ftp_server()
