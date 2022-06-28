from socket import *
import sys
import getpass
from _thread import *
import pickle
import os

ctrl_port = 12001
data_port = 11000
client_ip = '127.0.0.1'

def pwd(curr_dir, conn) :
	try :
		reply = '257 '+curr_dir+' is the current directory' 
		conn.send(reply.encode())
	except Exception as e:
		print(e)

def cd(conn, curr_dir, cmd) :
	if cmd[4:][0] == '/' :
		curr_dir = cmd[4:]
	else :
		curr_dir = curr_dir+'/'+cmd[4:]
	print(curr_dir)
	try :
		reply = '250 Directory changed successfully'
		conn.send(reply.encode())
	except Exception as e:
		print(e)
	return curr_dir

def ls(curr_dir, ctrl_conn) :
	try:
		data_conn = socket(AF_INET, SOCK_STREAM)
		data_conn.connect(('127.0.0.1', data_port))
		
		reply = '200 Port command Successful\n'+'150 Here comes the directory listing'
		ctrl_conn.send(reply.encode())
		
		filenameList = []
		for f in os.listdir(curr_dir) :
			filenameList.append(f)
		data = pickle.dumps(filenameList)
		data_conn.send(data)
		data_conn.close()

		reply = '226 Directory send OK'
		ctrl_conn.send(reply.encode())
	except :
		print('Error: Connection Refused')

def get(curr_dir, ctrl_conn, cmd) :
	
	try :
		data_conn = socket(AF_INET, SOCK_STREAM)
		data_conn.connect(('127.0.0.1', data_port))
		
		f = 'ftp_files/'+cmd[4:]
		fr = open(f, 'rb')
		
		l = fr.read(1024)
		while (l) :
			data_conn.send(l)
			l = fr.read(1024)
		fr.close()
	except Exception as e:
		print(e)
	
			
def put(curr_dir, ctrl_conn, cmd) :
	try :
		data_socket = socket(AF_INET, SOCK_STREAM)
		data_socket.bind(('', data_port))
		data_socket.listen(1)
		data_conn, addr = data_socket.accept()
		print('accepted')

		fname = cmd[4:]
		fr = open('ftp_files/'+fname, 'wb')
		
		l = data_conn.recv(1024)
		while(l) :
			fr.write(l)
			l = data_conn.recv(1024)
		fr.close()
		
		data_conn.close()
		data_socket.close()
	except Exception as e:
		print(e)

def quit(ctrl_conn) :
	try :
		ctrl_conn.close()
		ctrl_socket.close()
		exit()
	except Exception as e:
		print(e)

def mkdir(ctrl_conn, cmd, curr_dir) :
	try :
		if cmd[6] == '/' :
			os.mkdir(cmd[6:])
		else :
			os.mkdir(curr_dir+'/'+cmd[6:])
	except Exception as e:
		print(e)	
	
	
def clientThread(ctrl_conn, addr) :
	try :
		curr_dir = os.getcwd()
		msg = ctrl_conn.recv(1024)
		authorisation_data = pickle.loads(msg)
		recvd_user = authorisation_data['user']
		recvd_pswd = authorisation_data['pswd']
		if user == recvd_user and pswd == recvd_pswd :
			status = 'OK'
			ctrl_conn.send(status.encode())
		else :
			status = 'NOT_OK'
		while status == 'OK' :
			cmd = ctrl_conn.recv(1024).decode()
			if cmd.upper() == 'PWD' :
				pwd(curr_dir, ctrl_conn)
			if cmd[:2].upper() == 'CD' : 
				curr_dir = cd(ctrl_conn, curr_dir, cmd)
			if cmd[:4].upper() == 'LS' :
				ls(curr_dir, ctrl_conn)
			if cmd[:3].upper() == 'GET' :
				get(curr_dir, ctrl_conn, cmd)
			if cmd[:3].upper() == 'PUT' :
				put(curr_dir, ctrl_conn, cmd)
			if cmd[:4].upper() == 'QUIT' :
				quit(ctrl_conn)
			if cmd[:5].upper() == 'MKDIR' :
				mkdir(ctrl_conn, cmd, curr_dir)
			
	except Exception as e:
		print(e)
			
user = getpass.getuser()
pswd = 'anonymous'

ctrl_socket = socket(AF_INET, SOCK_STREAM)
ctrl_socket.bind(('', ctrl_port))
ctrl_socket.listen(1)

while True :
	ctrl_conn, addr = ctrl_socket.accept()
	start_new_thread(clientThread, (ctrl_conn, addr))
		


	
	
