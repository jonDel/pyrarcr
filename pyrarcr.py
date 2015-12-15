#!/usr/bin/python

#####      ##### ##### #####             ####   ####   #
#   # #  # #   # #   # #   # #### ####   #  #      #  ##
##### #### ##### ##### ##### #    #      #  #   ####   #
#       #  #  #  #   # #  #  #    #      #  #   #      #
#       #  #   # #   # #   # #### #      #### # #### # #

#finds the password of a desired rar or zip file using a brute-force algorithm

#importing needed modules
import time,os,sys,itertools, re
from multiprocessing import Pool
import subprocess

name=os.path.basename(__file__)

#checking if the user's operating system is compatible with pyrarcr
if os.name!="posix":
	print("ERROR:",name,"isn't compatible with your system.")
	sys.exit(-1)

def unrar(guessPass):
	global fileName
	cmd = ["unrar", "t", "-y" ,"-p"+guessPass, fileName]
	proc = subprocess.Popen( cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
	(stdout, stderr) = proc.communicate()
	if not stderr:
		print("Found password:",repr(guessPass))
		return True, guessPass
	return False, guessPass

def unzip(guessPass):
	global fileName
	cmd = ["7za", "t", "-y" ,"-p"+guessPass, fileName]
	proc = subprocess.Popen( cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
	(stdout, stderr) = proc.communicate()
	if re.match('.+?Everything is Ok',stdout, re.S):
		print("Found password:",repr(guessPass))
		return True, guessPass
	return False, guessPass


#defining the function
def rc(rf, alphabet, numOfThreads):
	tryn=0
	counterTmp = 0
	printCounter = 100
	listBasic = []
	if rf.endswith('.rar'):
		funcChosen = unrar
	elif rf.endswith('.zip') or rf.endswith('.7z') :
		funcChosen = unzip
	for a in range(1,len(alphabet)+1):
		for b in itertools.product(alphabet,repeat=a):
			k="".join(b)
			k=re.escape(k)
			listBasic.append(k)
			tryn+=1
			#tryn+=len(listBasic)
			counterTmp+=1
			if counterTmp >= printCounter:
				print ('Trying combination number '+str(tryn)+':'+str(k))
				timeWasted = round(time.time()-start,2)
				if timeWasted > 0:
					print("It took already ",timeWasted,"seconds. Speed: ",round(tryn/float(timeWasted),2)," passwords/sec")
				counterTmp=0
			if len(listBasic) == numOfThreads:
				pool = Pool(numOfThreads)
				result=pool.map(funcChosen, listBasic)
				pool.close()
				pool.join()
				for i in result:
					if True in i:
						print 'Found! Password is '+result[result.index(i)][1]
						print("It took",round(time.time()-start,3),"seconds")
						exit()
				listBasic = []

defaultAlphabet = "aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ1234567890"
defaultThreadNumbers= 2
name = sys.argv[0]
helpMessage = '''Usage:    '''+name+''' [rar file]
          '''+name+''' [rar file] [alphabet]
Examples: '''+name+''' foobar.rar
          '''+name+''' foobar.rar abc\~\(d1234567890\-'''

#checking if the file exists/running the function
argLen= len(sys.argv)
start=time.time()
if argLen >= 2:
	if not os.path.exists(sys.argv[1]):
		print("ERROR: File doesn't exist.\nExiting...")
	else:
		fileName = sys.argv[1]
		if argLen ==4:
			print ('Number of threads ='+str(sys.argv[3]))
			rc(sys.argv[1], sys.argv[2], int(sys.argv[3]))
		elif argLen ==3:
			print ('Number of threads ='+str(defaultThreadNumbers))
			rc(sys.argv[1], sys.argv[2], defaultThreadNumbers)
		elif argLen == 2:
			print ('Using default alphabet: '+defaultAlphabet)
			print ('Number of threads ='+str(defaultThreadNumbers))
			rc(sys.argv[1], defaultAlphabet, defaultThreadNumbers )
		else:
			print(helpMessage)
else:
	print(helpMessage)
