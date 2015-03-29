#!/usr/bin/env python
'''
Created on Jan 20, 2014

@author: magic282
'''

from SVPlayerHash import SVPlayerHash
try:  # Python 3
    from urllib.parse import urlencode
    from urllib.request import Request, urlopen
except ImportError:  # Python 2
    from urllib import urlencode
    from urllib2 import Request, urlopen
import json

# from guess_language import guessLanguage,guessLanguageTag,guessLanguageName,guessLanguageId,guessLanguageInfo
import chardet
import os
from lang_detect import zh2utf8,lang_detect
from utf8sc2tc import utf8_sc2tc

##lang_wanted = ["en","zh"]
##encoding_wanted = ['UTF-16LE','GB2312','Big5']

class Shooter(object):
    '''
    classdocs
    '''

    __SHOOTERURL = "http://shooter.cn/api/subapi.php"

    __fileName = ""
    __videoHash = ""

    __subInfo = []



    def start(self):
        try:
            print("=================================")
            print "Processing: %s ..." % os.path.basename(self.__fileName)
            self.__videoHash = SVPlayerHash.ComputeFileHash(self.__fileName)
        except:
            print(">>File Access Error.")
            return False

        values = dict(filehash=self.__videoHash, pathinfo=self.__fileName, format="json", lang="Chn")
##        values = dict(filehash=self.__videoHash, pathinfo=self.__fileName.encode("utf8"), format="json", lang="Chn")
        data = urlencode(values).encode('utf-8', 'replace')
        req = Request(self.__SHOOTERURL, data)
        try:
            rsp = urlopen(req)
            content = rsp.read().decode('utf-8', 'replace')
        except:
            print ">>Connection Error"
            return False

        jsonContent = ""
        try:
            # print "json loading...",
            jsonContent = json.loads(content)
            # print "Done"
        except:
            print(">>No Subtitle Found.")
            return False

        # count=0
        # for idx, i in enumerate(jsonContent):
        #     count = count+1
        # print(">>Total %s Subtitles Found."%count)

        res = False
        extcnt={}
        for idx_i, i in enumerate(jsonContent):
            #print(i)

            lang=""

            for idx_j, j in enumerate(i["Files"]):
                dLink = j["Link"]
                #print(dLink)
                response = urlopen(dLink)
                backF = response.read()

                if j["Ext"]=="ass":
                    lang="zh"
                    d=chardet.detect(backF[:300])
                    if d["encoding"]:
                        c=d["encoding"].lower()
                        backF=utf8_sc2tc(zh2utf8(backF,c).decode("utf8"))
                        print ">>Lang %s, because of extension .%s, %s convert to utf8(big5)" % (lang,j["Ext"],c)
                    else:
                        print ">>Lang %s, because of extension .%s" % (lang,j["Ext"])
                elif j["Ext"]=="idx":
                    lang=""
                    print ">>Lang none, because of extension .%s" % j["Ext"]
                elif j["Ext"]=="sub" and len(backF) > 1000000:
                    lang=""
                    print ">>Lang none, because of extension .%s" % j["Ext"]
                else:
                    print ">> Testing  %s.%s" % (os.path.splitext(os.path.basename(self.__fileName))[0],str(j["Ext"]))
                    d=chardet.detect(backF[:300])
                    if d["encoding"] == None:
                        print ">>Encoding not found"
                        continue
                    c=d["encoding"].lower()

                    big5Codec = ["big5"]
                    gbCodec = ["gb2312","gbk"]
                    unicodeCodec = ['utf-8','utf-8-sig',"utf-16le","utf-16be"]
                    unicodeLikelyKeep = ["big5","gb2312","gbk"]
                    unicodegb = ["gb2312","gbk"]

                    if c == 'ascii':
                        lang="eng"
                        print ">>Lang %s, because of encoding"%lang,c
                    elif c in gbCodec:
                        backF=utf8_sc2tc(zh2utf8(backF,c).decode("utf8"))
                        lang="zh"
                        print ">>Lang %s, because of encoding %s, convert to utf8(big5)"%(lang,c)
                    elif c in big5Codec:
                        backF=zh2utf8(backF,c)
                        lang="zh"
                        print ">>Lang %s, because of encoding %s, convert to utf8"%(lang,c)
                    elif c in unicodeCodec:
                        enc,likely = lang_detect(backF)
##                        print c,enc,likely
                        if likely == "ascii":
                            lang="eng"
                            print ">>Lang %s, because of encoding %s(%s)"%(lang,c,likely)
                        elif likely not in unicodeLikelyKeep:
                            print ">>Lang unknown, because of encoding %s(%s)"%(c,likely)
                            continue
                        elif likely in unicodegb:
                            lang="zh"
                            backF=utf8_sc2tc(backF.decode(c))
                            print ">>Lang %s, because of encoding %s(%s), convert to utf8(big5)"%(lang,c,likely)
                        else:
                            lang="zh"
                            print ">>Lang %s, because of encoding %s(%s)"%(lang,c,likely)
                    else:
                        print ">>Lang unknown, because of encoding",c
                        continue

                index = 0
                ext = lang + "." + j["Ext"]
                if ext in extcnt:
                    extcnt[ext] = extcnt[ext]+1
                    index = extcnt[ext]
                else:
                    extcnt[ext]=0

                # print ext,index

                outFileNameList = [os.path.splitext(self.__fileName)[0], "%s%s" % (lang,("" if index == 0 else index)), str(j["Ext"])]
                if len(i["Files"]) != 1: outFileNameList.insert(2, str(idx_i))
                outFileName = '.'.join(outFileNameList)
                print "   Writing:",os.path.basename(outFileName)
                with open(outFileName, 'wb') as output: output.write(backF)
                res = True

                if i["Delay"] != 0:
                    delayFileName = '.'.join((os.path.splitext(self.__fileName)[0], "%s%s" % (lang,("" if index == 0 else index)), "delay"))
                    with open(delayFileName, 'w') as output: output.write(str(i["Delay"]))
                    print "   Writing:",os.path.basename(delayFileName)

##        if (res): print " Found for: %s" % os.path.basename(self.__fileName)
        # print "Returning", res
        return res


    def __init__(self, params):
        '''
        Constructor
        '''
        self.__fileName = params
