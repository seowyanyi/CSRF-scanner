import json
import urllib
import urllib2
import ssl
import sys
from urlparse import urlparse
import os


class Phase3(object):

    def __init__(self, inputFilename, outputDir, baseFileName):
        self.filename = inputFilename
        self.fileObj = open(self.filename, "r")
        self.outputDir = outputDir
	if not os.path.exists(self.outputDir):
	    os.makedirs(self.outputDir)
	self.outputFilename = self.outputDir + baseFileName
        self.outputfileObj = open(self.outputFilename, "w")

    def linkDetailExtractor(self, linkDetails):
        method = linkDetails["method"]
        action = ""
        params = ""
        href = ""
        try:
            href = linkDetails["href"]
        except Exception:
            #print ("no href")
            href = ""
        try:
            action = linkDetails["action"]
        except Exception:
            #print ("no action")
            action = ""
        try:
            params = linkDetails["params"]
        except Exception:
            #print ("no params")
            params = ""
        return method, action, params, href

    def login(self, url, loginCredential,appName):
        try:
            parsed_url = urlparse(url)
            domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_url)
            #print domain
            dataU = urllib.urlencode(loginCredential)
            #context = ssl._create_unverified_context()
            req = urllib2.Request(url, dataU)
            res = urllib2.urlopen(req)
            #print ("login details code: {}".format(res.code))
            cookie = res.info()['Set-Cookie']
            return (cookie, domain)
        except Exception, e:
            print "Exception in Logging in"
            print appName
            return ("",domain)


    def resolveParams(self,parameters):
        type = parameters["type"]
        if type == "reset" or type == "submit":
            return ("","","")

        name = parameters["name"]
        value = parameters["value"]
        return (type, name, value)

    def getPostParams(self,parameters):
        values = {}
        if parameters:
            for param in parameters:
                (type,name,value) = self.resolveParams(param)
                if type != "":
                    values[name] = value
                return values

    def makeRequest(self,url,method,parameters,href,domain):
        if method.upper() == "POST":
            if (domain not in url):
                url = domain + url
            if len(parameters) != 0:
                #print ("In post method")
                dataU = self.getPostParams(parameters)
                dataU = urllib.urlencode(dataU)
                try:
                    req = urllib2.Request(url,dataU)
                    #print ("pass req")
                    req.add_header("Cookier",self.cookie)
                    #print ("pass adding cookie")
                    try:
                        #context = ssl._create_unverified_context()
                        res = urllib2.urlopen(req)
                        #print ("pass urlopen code: {}".format(res.code))
                    except urllib2.URLError, e:
                        #print e.code
                        return (False,e.code,"")
                except Exception, e:
                    #print "Exception in makeRequest POST"
                    import traceback
                   # print traceback.format_exc()
                   # print url
                    return (False, e, "")
                #print ("No exception in POST")
                return (True,res,method)
            else:
                return (False, "", "")
        elif method.upper() == "GET":
            if (domain not in href):
                href = domain + href
            if href != "":
                #print href
                #print ("In get method")
                try:
                    req = urllib2.Request(href)
                   # print ("pass req")
                    req.add_header("Cookier", self.cookie)
                    #print ("pass adding cookie")
                    try:
                        #context = ssl._create_unverified_context()
                        res = urllib2.urlopen(req)
                        #print ("pass urlopen code: {}".format(res.code))
                    except urllib2.URLError, e:
                        return (False, e.code, "")
                except Exception, e:
                    #print "Exception in makeRequest GET"
                    import traceback
                   # print traceback.format_exc()
                   # print url
                    return (False, e, "")
                #print ("No exception in GET")
                return (True, res, method)
            elif url != "":
                if (domain not in url):
                    url = domain + url
                if len(parameters) != 0:
                    #print ("In get with action method")
                    dataU = self.getPostParams(parameters)
                    dataU = urllib.urlencode(dataU)
                    try:
                        req = urllib2.Request(url, dataU)
                        #print ("pass req")
                        req.add_header("Cookier", self.cookie)
                        #print ("pass adding cookie")
                        try:
                            #context = ssl._create_unverified_context()
                            res = urllib2.urlopen(req)
                            #print ("pass urlopen code: {}".format(res.code))
                        except urllib2.URLError, e:
                            return (False, e.code,"")
                    except Exception, e:
                        #print "Exception in makeRequest GET"
                        import traceback
                       # print traceback.format_exc()
                       # print url
                        return (False, e,"")
                    #print ("No exception in GET")
                    return (True, res,method)
                else:
                    return (False, "","")
            else:
                return (False, "","")
        else:  #trying both POST and GET
            #print ("trying both post and get")
            if (domain not in url):
                url = domain + url
            if url != "" and len(parameters) != 0:
               # print ("In post method")
                dataU = self.getPostParams(parameters)
                dataU = urllib.urlencode(dataU)
                try:
                    req = urllib2.Request(url,dataU)
                    #print ("pass req")
                    req.add_header("Cookier",self.cookie)
                   # print ("pass adding cookie")
                    try:
                        #context = ssl._create_unverified_context()
                        res = urllib2.urlopen(req)
                        #print ("pass urlopen code: {}".format(res.code))
                    except urllib2.URLError, e:
                        return (False,e.code,"")
                except Exception, e:
                    #print "Exception in makeRequest POST"
                    import traceback
                   # print traceback.format_exc()
                   # print url
                    return (False, e,"")
                #print ("No exception in POST")
                return (True,res,"post")
            elif href != "":
                if (domain not in href):
                    href = domain + href
               # print ("In get method")
                try:
                    req = urllib2.Request(href)
                   # print ("pass req")
                    req.add_header("Cookier", self.cookie)
                    #print ("pass adding cookie")
                    try:
                        #context = ssl._create_unverified_context()
                        res = urllib2.urlopen(req)
                        #print ("pass urlopen code: {}".format(res.code))
                    except urllib2.URLError, e:
                        return (False, e.code,"")
                except Exception, e:
                    #print "Exception in makeRequest GET"
                    import traceback
                   # print traceback.format_exc()
                   # print url
                    return (False, e,"")
                #print ("No exception in GET")
                return (True, res,"get")
            else:
                #print ("not in any category")
                return (False,"","")




    def startPhase3(self):
        jsonStr = self.fileObj.read()
        data = json.loads(jsonStr)

        count = 1;

        xdata = []
        for appData in data:
            xappData = {}
            xappDetails = []
            xwebData = {}
            appDetailsFlag = False
            appName = appData["AppName"]
            loginCredential = appData["Login"]
            loginUrl = appData["LoginLink"]
            print ("logging in!")
            #print (appName)
            (self.cookie, self.domain) = self.login(loginUrl, loginCredential,appName)
            appDetails = appData["AppDetails"]
            for webData in appDetails:
                xwebPageLinks = []
                weblinkFlag = False
                webPage = webData["WebPage"]
                webPageLinks = webData["WebPageLinks"]
                for linkDetails in webPageLinks:
                    (method, action, params, href) = self.linkDetailExtractor(linkDetails)
                    print "Count at: {}".format(count)
                    (result, res, method) = self.makeRequest(action,method,params,href,self.domain)
                    count += 1
                    linkDetails["method"] = method
                    if result == True:
                        xwebPageLinks.append(linkDetails)
                        weblinkFlag = True
                if weblinkFlag == True:
                    xwebData["WebPageLinks"] = xwebPageLinks
                    xwebPageLinks = []
                    xwebData["WebPage"] = webPage
                    xappDetails.append(xwebData)
                    xwebData = {}
                    appDetailsFlag = True
            if appDetailsFlag == True:
                xappData["AppDetails"] = xappDetails
                xappDetails = []
                xappData["LoginLink"] = loginUrl
                xappData["Login"] = loginCredential
                xappData["AppName"] = appName
                xdata.append(xappData)
                xappData = {}
        json.dump(xdata, self.outputfileObj, indent=4)



if __name__ == "__main__":

    obj = Phase3(sys.argv[1],sys.argv[2], sys.argv[3])
    obj.startPhase3()
