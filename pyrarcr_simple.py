#!/usr/bin/python

#####      ##### ##### #####             ####   ####   #
#   # #  # #   # #   # #   # #### ####   #  #      #  ##
##### #### ##### ##### ##### #    #      #  #   ####   #
#       #  #  #  #   # #  #  #    #      #  #   #      #
#       #  #   # #   # #   # #### #      #### # #### # #

#finds the password of a desired rar or zip file using a brute-force algorithm

#importing needed modules
import time,os,sys,itertools, re
from zipfile import ZipFile

name=os.path.basename(__file__)

#checking if the user's operating system is compatible with pyrarcr
if os.name!="posix":
	print("ERROR:",name,"isn't compatible with your system.")
	sys.exit(-1)

#defining the function
def tryPassword(compressedFile, alphabet):
	start=time.time()
	tryn=0
	counterTmp = 0
	printCounter = 10000
	for a in range(1,len(alphabet)+1):
		for b in itertools.product(alphabet,repeat=a):
			guessPass="".join(b)
			guessPass=re.escape(guessPass)
			with ZipFile(compressedFile, 'r') as myzip:
				try:
					myzip.extractall('/tmp', None, guessPass)
				except:
					ret = False
				else:
					ret = True

			tryn+=1
			if ret:
				print("Found password:",repr(guessPass))
				print("Tried combination count:",tryn)
				print("It took",round(time.time()-start,3),"seconds")
				print("Speed: ",tryn/float(time.time()-start)," passwords/sec")
				print("Exiting...")
				time.sleep(2)
				sys.exit(0)
			counterTmp+=1
			if counterTmp >= printCounter:
				print ('Trying combination number '+str(tryn)+':'+str(guessPass))
				timeWasted = round(time.time()-start,2)
				print("It took already ",timeWasted,"seconds. Speed: ",round(tryn/timeWasted,2)," passwords/sec")
				counterTmp=0

defaultAlphabet = "aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ1234567890"
name = sys.argv[0]
helpMessage = '''Usage:    '''+name+''' [rar file]
          '''+name+''' [rar file] [alphabet]
Examples: '''+name+''' foobar.rar
          '''+name+''' foobar.rar abc\~\(d1234567890\-'''

#checking if the file exists/running the function
argLen= len(sys.argv)
if argLen >= 2:
	if not os.path.exists(sys.argv[1]):
		print("ERROR: File doesn't exist.\nExiting...")
	else:
		if argLen ==3:
			tryPassword(sys.argv[1], sys.argv[2])
		elif argLen == 2:
			print ('Using default alphabet: '+defaultAlphabet)
			tryPassword(sys.argv[1], defaultAlphabet )
		else:
			print(helpMessage)
else:
	print(helpMessage)


