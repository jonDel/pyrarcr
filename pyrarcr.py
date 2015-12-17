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
from zipfile import ZipFile

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
		global start
		print "It took "+str(time.time-start)+" seconds"
		return True, guessPass
	return False, guessPass

def unzip(guessPass):
	global fileName
	okOutput = '0\n'
	cmd='7za t -y -p'+guessPass+' '+fileName+' > /dev/null ;echo $?'
	kf=os.popen(cmd)
	for rkf in kf.readlines():
		if rkf == okOutput:
			print("Found password:",repr(guessPass))
			print("It took",round(time.time()-start,3),"seconds")
			print("Exiting...")
			return True, guessPass
	return False, guessPass


#defining the function
def rc(rf, alphabet, numOfThreads):
	tryn=0
	counterTmp = 0
	printCounter = 1000
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
			if len(listBasic) == numOfThreads:
				pool = Pool(numOfThreads)
				pool.map_async(funcChosen, listBasic, callback = exitPass)
				pool.close()
				if resultPass:
					timeWasted = time.time()-start
					print 'Found! Password is '+resultPass
					print "It took " +str(round(time.time()-start,3))+" seconds"
					print "Speed: "+str(round(tryn/float(timeWasted),2))+" passwords/sec"
					print "Tried "+str(tryn)+" passwords"
					exit()
				listBasic = []
			counterTmp+=1
			if counterTmp >= printCounter:
				print 'Trying combination number '+str(tryn)+':'+str(k)
				timeWasted = round(time.time()-start,2)
				if timeWasted > 0:
					print "It took already " +str(timeWasted) +" seconds. Speed: "+str(round(tryn/float(timeWasted),2))+" passwords/sec"
				counterTmp=0

def exitPass(result):
	for results in result:
		if True in results:
			global resultPass
			resultPass = results[1]

resultPass = None
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


def fucsia (fileName, passwd):
	start = time.time()
	with ZipFile(fileName, 'r') as myzip:
		try:
			myzip.extractall('/tmp', None, passwd)
		except Exception as error:
			print str(error)
			print 'senha podre'
	print (time.time()-start)

