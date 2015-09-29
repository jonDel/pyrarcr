#!/usr/bin/python

#####      ##### ##### #####             ####   ####   #
#   # #  # #   # #   # #   # #### ####   #  #      #  ##
##### #### ##### ##### ##### #    #      #  #   ####   #
#       #  #  #  #   # #  #  #    #      #  #   #      #
#       #  #   # #   # #   # #### #      #### # #### # #

#finds the password of a desired rar or zip file using a brute-force algorithm

#importing needed modules
import time,os,sys,shutil,itertools, re

name=os.path.basename(__file__)

#checking if the user's operating system is compatible with pyrarcr
if os.name!="posix":
 print("ERROR:",name,"isn't compatible with your system.")
 sys.exit(-1)
#checking if the user has unrar/p7zip installed
for which in ["unrar","p7zip"]:
 if not shutil.which(which):
  print("ERROR:",which,"isn't installed.\nExiting...")
  sys.exit(-1)

#defining the function
def rc(rf, alphabet):
 start=time.time()
 tryn=0
 counterTmp = 0
 printCounter = 1000
 for a in range(1,len(alphabet)+1):
  for b in itertools.product(alphabet,repeat=a):
   k="".join(b)
   k=re.escape(k)
   if rf[-4:]==".rar":
    cmd = "unrar t -y -p%s %s 2>&1|grep 'All OK'"%(k,rf)
    kf=os.popen(cmd)
    tryn+=1
    counterTmp+=1
    if counterTmp >= printCounter:
      print ('Trying combination number '+str(tryn)+':'+str(k))
      timeWasted = round(time.time()-start,2)
      print("It took already ",timeWasted,"seconds. Speed: ",round(tryn/timeWasted,2)," passwords/sec")
      counterTmp=0
    for rkf in kf.readlines():
     if rkf=="All OK\n":
      print("Found password:",repr(k))
      print("Tried combination count:",tryn)
      print("It took",round(time.time()-start,3),"seconds")
      print("Exiting...")
      time.sleep(2)
      sys.exit(1)
   elif rf[-4:]==".zip" or rf[-3:]==".7z":
    kf=os.popen("7za t -p%s %s 2>&1|grep 'Everything is Ok'"%(k,rf))
    tryn+=1
    counterTmp+=1
    if counterTmp >= printCounter:
      print ('Trying combination number '+str(tryn)+':'+str(k))
      timeWasted = round(time.time()-start,2)
      print("It took already ",timeWasted,"seconds. Speed: ",round(tryn/timeWasted,2)," passwords/sec")
      counterTmp=0
    for rkf in kf.readlines():
     if rkf=="Everything is Ok\n":
      print("Found password:",repr(k))
      print("Tried combination count:",tryn)
      print("It took",round(time.time()-start,3),"seconds")
      print("Exiting...")
      time.sleep(2)
      sys.exit(1)
   else:
    print("ERROR: File isnt a RAR, ZIP or 7z file.\nExiting...")

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
      rc(sys.argv[1], sys.argv[2])
    elif argLen == 2:
      print ('Using default alphabet: '+defaultAlphabet)
      rc(sys.argv[1], defaultAlphabet )
    else:
      print(helpMessage)
else:
  print(helpMessage)
