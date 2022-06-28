from socket import *
import sys
import getpass
import pickle
import os

state = 'not_connected'

ctrl_socket = socket(AF_INET, SOCK_STREAM)

ctrl_port = 12001
data_port = 11000

def connect() :
	args = input('(to)').split()
	if len(args) != 2 :
		print('Enter ip address and port number')
		sys.exit()
	else :
		try :
			ctrl_socket.connect((args[0], int(args[1])))
			print('Connected to '+args[0])
			user = input('User: ')
			pswd = getpass.getpass()
			data_to_send = {'user': user, 'pswd' : pswd}
			msg = pickle.dumps(data_to_send)
			ctrl_socket.send(msg)
			status = ctrl_socket.recv(1024).decode()
			if status == 'OK' :
				print('Login Successful')
				print('Remote system type is UNIX.\nUsing binary mode to transfer files.')
				global state 
				state = 'connected'
			else :
				print('Login failed')
		except Exception as e:
			print(e)
		
	
		
def pwd() :
	cmd = 'pwd'
	try :
		ctrl_socket.send(cmd.encode())
		reply = ctrl_socket.recv(1024).decode() 
		print(reply)
	except Exception as e:
		print(e)
		

def cd(cmd) :
	try :
		directory = cmd[2:]
		data_to_send = 'cd'+' '+directory
		ctrl_socket.send(data_to_send.encode())
		reply = ctrl_socket.recv(1024).decode()
		print(reply)
	except Exception as e :
		print(e)

def ls() :
	try :
		ctrl_socket.send(cmd.encode())
		
		data_socket = socket(AF_INET, SOCK_STREAM)
		data_socket.bind(('', data_port))
		data_socket.listen(1)
		data_conn, addr = data_socket.accept()
		print('accepted')

		reply = ctrl_socket.recv(1024).decode()
		print(reply)
		
		msg = data_conn.recv(1024)
		data = pickle.loads(msg)
		for f in data :
			print(f)
		data_conn.close()
		data_socket.close()
		
		reply = ctrl_socket.recv(1024).decode()
		print(reply)
	except Exception as e:
		print(e)
	
def get(cmd, curr_dir) :
	try :
		ctrl_socket.send(cmd.encode())

		data_socket = socket(AF_INET, SOCK_STREAM)
		data_socket.bind(('', data_port))
		data_socket.listen(1)
		data_conn, addr = data_socket.accept()
		print('accepted')

		fname = cmd[4:]
		fr = open('ftp_downloads/'+fname, 'wb')
		
		l = data_conn.recv(1024)
		while(l) :
			fr.write(l)
			l = data_conn.recv(1024)
		fr.close()
		data_conn.close()
		data_socket.close()
	except Exception as e:
		print(e)
			
def put(cmd, curr_dir) :
	try :
		ctrl_socket.send(cmd.encode())

		data_conn = socket(AF_INET, SOCK_STREAM)
		data_conn.connect(('127.0.0.1', data_port))
		
		f = curr_dir+'/ftp_downloads/'+cmd[4:]
		fr = open(f, 'rb')
		
		l = fr.read(1024)
		while (l) :
			data_conn.send(l)
			l = fr.read(1024)
		fr.close()
	except Exception as e:
		print(e)

def quit(cmd) :
	try :
		ctrl_socket.send(cmd.encode())
	except Exception as e:
		print(e)
def mkdir(cmd) :
	try :
		ctrl_socket.send(cmd.encode())
	except Exception as e:
		print(e)

def lcd(cmd, curr_dir) :
	try :
		if len(cmd) > 3 :
			curr_dir += '/'+cmd[4:]
		print('Local directory now '+curr_dir)
	except Exception as e:
		print(e)

def close() :
	try :
		ctrl_socket.close()
		global state
		state = 'not connected'
	except Exception as e:
		print(e)
while True :
	curr_dir = os.getcwd()
	cmd = input('ftp>')
	if cmd.lower() == 'open' :
		connect()
	elif cmd.lower() == 'pwd' and state == 'connected':
		pwd() 
	elif cmd[:2].lower() == 'cd' and state == 'connected':
		cd(cmd)
	elif cmd.lower() == 'ls' and state == 'connected' :
		ls()
	elif cmd[:3].lower() == 'get' and state == 'connected' :
		get(cmd, curr_dir)
	elif cmd[:3].lower() == 'put' and state == 'connected' :
		put(cmd, curr_dir)
	elif cmd[:4].lower() == 'quit':
		quit(cmd)
	elif cmd[:5].lower() == 'mkdir' and state == 'connected' :
		mkdir(cmd)
	elif cmd[:3].lower() == 'lcd' and state == 'connected' :
		lcd(cmd, curr_dir)
	elif cmd.lower() != 'open' and state == 'not_connected' :
		print('Connect with server with open function')
	elif cmd.lower() == 'close' and state == 'connected' :
		close()
	else :
		print('Enter commands: open\ncd\nls\nget\nput\nquit\nmkdir\nlcd')
			

				

			
		
			
		
			
	
