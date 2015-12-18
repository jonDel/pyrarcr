#!/usr/bin/python

#####      ##### ##### #####             ####   ####   #
#   # #  # #   # #   # #   # #### ####   #  #      #  ##
##### #### ##### ##### ##### #    #      #  #   ####   #
#       #  #  #  #   # #  #  #    #      #  #   #      #
#       #  #   # #   # #   # #### #      #### # #### # #

#finds the password of a desired rar or zip file using a brute-force algorithm

#importing needed modules
import time,os,sys,itertools, re
from zipfileMod import ZipFile

name=os.path.basename(__file__)

#checking if the user's operating system is compatible with pyrarcr
if os.name!="posix":
	print("ERROR:",name,"isn't compatible with your system.")
	sys.exit(-1)


def unzip(compressedFile,guessPass):
  okOutput = '0\n'
  cmd='7za t -y -p'+guessPass+' '+compressedFile+' > /dev/null ;echo $?'
  kf=os.popen(cmd)
  for rkf in kf.readlines():
    if rkf == okOutput:
      return True
  return False

#defining the function
def tryPassword(compressedFile, alphabet):
	start=time.time()
	tryn=0
	falsePos=0
	counterTmp = 0
	printCounter = 10000
	for a in range(1,len(alphabet)+1):
		for b in itertools.product(alphabet,repeat=a):
			guessPass="".join(b)
			guessPass=re.escape(guessPass)
			with ZipFile(compressedFile, 'r') as myzip:
				ret = myzip.testPwd(guessPass)
			tryn+=1
			if ret:
				# BUG in zipfile lib: 1 in 256 times prob of false positives
				# so it faster to recheck the false positives with 7za
				if unzip(compressedFile, guessPass):
					print "Found password:"+str(repr(guessPass))
					print "Tried combination count: "+str(tryn)
					print "It took "+str(round(time.time()-start,3))+" seconds"
					print "Speed: "+str(tryn/float(time.time()-start))+" passwords/sec"
					print 'False positives: '+str(falsePos)
					print 'False positives chances: '+str((falsePos/float(tryn))*100)+' %'
					print("Exiting...")
					time.sleep(2)
					sys.exit(0)
				else:
					falsePos+=1
			counterTmp+=1
			if counterTmp >= printCounter:
				print 'Trying combination number '+str(tryn)+':'+str(guessPass)
				timeWasted = round(time.time()-start,2)
				print 'False positives: '+str(falsePos)
				print"It took already "+str(timeWasted)+" seconds. Speed: "+str(round(tryn/timeWasted,2))+" passwords/sec"
				counterTmp=0

defaultAlphabet = "aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ1234567890"
name = sys.argv[0]
helpMessage = '''Usage:    '''+name+''' [rar file]
          '''+name+''' [rar file] [alphabet]
Examples: '''+name+''' foobar.rar
          '''+name+''' foobar.rar abc\~\(d1234567890\-'''


##TODO: not implemented types : check reference: https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT
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


