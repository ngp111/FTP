from socket import *
import sys
import pickle

ctrl_port = 12000

class ftp_client() :
	def __init__(self) :
		self.ctrl_socket = socket(AF_INET, SOCK_STREAM)
		self.curr_dir = '/home/hp/init/client/ftp_downloads'
		while(True) :
			cmd = input("ftp> ")
			if cmd.lower() == 'open' :
				self.connect()
			
	def connect(self) :
		try :
			self.ctrl_socket.connect((args, ctrl_port))
			print("Connection Established with server")
		except ConnectionRefusedError:
			print('connect: Connection Refused')

	
		
		
	
			
		
if __name__ == '__main__' :
	client = ftp_client()


