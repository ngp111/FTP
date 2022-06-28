str = input()
if str.lower() == "ftp" :
	termprompt()

def termprompt() :
    PS1="${PS1//@\\h/}"     # Remove @host
    PS1="${PS1//\\w/\\W}"   # Change from full directory to last name

