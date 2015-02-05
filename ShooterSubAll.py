#!/usr/bin/python

import os
import sys
from time import time
from datetime import timedelta
import traceback
# import ntpath
from Shooter import Shooter
import lang_detect

##exclude_ext = ["chn", "eng", ".nfo", ".jpg", ".idx", ".sub"]
exclude_ext = ["zh", "eng", ".nfo", ".jpg", ".idx", ".sub"]
##sub_ext = ["chn.srt", "chn.ass", "chn.ssa", ".idx", ".sub"]
sub_ext = ["zh.srt", "zh.ass", "zh.ssa", ".idx", ".sub"]

##has_list = ["chn.srt", "chn.ass", "chn.ssa"]
has_list = ["zh.srt", "zh.ass", "zh.ssa"]
del_list = [".idx", ".sub"]

maxAgeDays = 7

# suball <dir> [mp4, mkv, avi]
# subtitle clean xxx.mp4 chn eng .nfo .jpg

def subtitleClean(file, exclude_keywords):
	filename =os.path.splitext(os.path.basename(file))[0]
	filepath = os.path.join(os.path.abspath('.'),os.path.dirname(file))

	for f in os.listdir(filepath):
		if filename in f:
			# print f
			seleted = True
			for keyword in exclude_keywords:
				if keyword in f: seleted = False
			if os.path.basename(file) == f: seleted = False
			if seleted:
				print "  Deleting:",f
				fullname = os.path.join(filepath,f)
				# print "Deleting",fullname
				# print os.path.abspath(f)
				try:
					os.remove(fullname)
				except:
					print ">>Delete failed"


def subtitleCleanIdxSub(file,ifhasthese,delthese):
	filename_noext =os.path.splitext(os.path.basename(file))[0]
	filepath = os.path.dirname(file)

	has = False
	for f in os.listdir(filepath):
		if filename_noext in f:
			for keyword in ifhasthese:
				if keyword in f: has = True
	if has:
		for f in os.listdir(filepath):
			if filename_noext in f:
				for keyword in delthese:
					if keyword in f:
						print "  Deleting:",f
						fullname = os.path.join(filepath,f)
						try:
							os.remove(fullname)
						except:
							print ">>Delete failed"


def shootSub(file,nosub_list):
	shooter = Shooter(file)
	ok = shooter.start()
	if ok: subtitleClean(file, exclude_ext)
	else: nosub_list.append(os.path.basename(file))


def ignoreAdd(file,ignorefile):
    filename=os.path.basename(file)
##    print("filedate test:",filename)#.encode("big5",'ignore'))
    try:
        if os.path.getmtime(file) < time()-timedelta(maxAgeDays).total_seconds():
            if ignorefile:
                print "Ignore Add:",filename
                open(ignorefile,"a").writelines(filename+"\n")
##            else:
##                print("ignore error:",ignorefile)
##        else:
##            print("filedate not old:",filename)
    except:
        print ">>Ignore Add Error,",filename
        pass


# shooterFile(file)
#     if file has no filename.chn.srt or filename.chn.ass
#       shootdownloader.exe file
#       if errorlevel == 0
#         shooterclean.exe file chn eng .nfo .jpg
#       else
#         nosub.list add(file)

def shooterFile(file, sub_keywords, nosub_list,ignorefile):
	filename = os.path.splitext(os.path.basename(file))[0]
	filepath = os.path.dirname(file)

	subbed = False
	for f in os.listdir(filepath):
		if filename in f:
			for sub in sub_keywords:
				if sub in f: subbed = True
	if not subbed:
		# # print "Process",os.path.basename(file)
		# # ok = False
		# # fullname = os.path.join(filepath,f)
		# shooter = Shooter(file)
		# ok = shooter.start()
		# if ok: subtitleClean(file, exclude_ext)
		# else: nosub_list.append(os.path.basename(file))
		shootSub(file,nosub_list)
		ignoreAdd(file,ignorefile)
	else:
		subtitleClean(file, exclude_ext)


# shooterListAll(root)
#   for each dir in root
#     if each file in videofile
#       if file not in ignore.list
#         shootsub(file)

def shooterListAll(path, ext_list, ignore_list,ignorefile):
	# for item in os.listdir(path):
	# 	# print "item",item
	# 	fullname = os.path.join(path,item)
	# 	# print fullname
	# 	if os.path.isfile(item):
	# 		print "File:",fullname
	# 	if os.path.isdir(item):
	# 		print "Entering", fullname
	# 		shooterdir(fullname,ext)
	nosub_list = []

	if os.path.isfile(path):
		# print os.path.dirname(path)
		# shooterSub(path,sub_ext,nosub_list)
		subtitleCleanIdxSub(path,has_list,del_list)
		shootSub(path,nosub_list)
	else:
		for root, dirs, files in os.walk(path):
		    # print root
		    for f in files:
		        # print os.path.join(root, f)
		        # print f
		        for ext in ext_list:
		        	if ext in os.path.splitext(f)[1]:
		        		# print f
		        		if f in ignore_list:
		        			print("=================================")
		        			print "  Ignoring:", f
		        		else:
		        		# if not f in ignore_list:
		        			# print "Processing:", f
		        			subtitleCleanIdxSub(os.path.join(root, f),has_list,del_list)
		        			shooterFile(os.path.join(root, f),sub_ext,nosub_list,ignorefile)
		        			continue

	print "================="
	print "File without sub:"
	for f in nosub_list:
	   print f
##	   print "      NONE:",f


def shooterCleanAll(path, hasthis, delthis):
	if os.path.isfile(path):
		subtitleCleanIdxSub(path,hasthis,delthis)
	else:
		for root, dirs, files in os.walk(path):
		    # print root
		    for f in files: subtitleCleanIdxSub(os.path.join(root, f),hasthis,delthis)


def getListFromFile(file):
	list1 = open(file,"r").readlines()
	list2 = []
	for item in list1:
		list2.append(item.strip())
##		list2.append(unicode(item.strip()))
	return list2


def usage():
	print("========================")
	print("Welcome to ShooterSubAll")
	print("========================")
	app = os.path.basename(sys.argv[0])
	print app, "[Directory or Filename]", "[Ignored File List]", "[Video file extensions]"
	print "Examples:", app, "xxx.mkv"
	print "Examples:", app, "TV/", "ignore.txt", "avi mkv mp4"

def main():
	try:
		dirNames = sys.argv[1]
##		dirNames = lang_detect.unicode(sys.argv[1])
		video_list = sys.argv[3:]
	except:
		usage()
		return

	ignorefile = None
	try:
		file = sys.argv[2]
		ignorefile = os.path.abspath(file)
		ignore_list = getListFromFile(ignorefile)
		print "Ignored %s Entries" % len(ignore_list)
	except:
##		traceback.print_exc()
		ignore_list = []

	# shooterCleanAll(os.path.abspath(dirNames),has_list,del_list)
	shooterListAll(os.path.abspath(dirNames), video_list,ignore_list,ignorefile)

if __name__ == '__main__':
	main()
