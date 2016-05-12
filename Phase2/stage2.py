import json, sys, os


def main(argv,appName):
    fileobj = open("Phase1/output/" +appName + "/" + argv, "r")
    mainList = []
    jsonstr = fileobj.read()
    jsonObj = json.loads(jsonstr)
    for eachApp in jsonObj:
        mainDic = {}
        mainDic['AppName'] = eachApp['AppName']
        mainDic['LoginLink'] = eachApp['LoginLink']
        mainDic['Login'] = {}
        mainDic['Login']['user_id'] = eachApp['Login']['user_id']
        mainDic['Login']['password'] = eachApp['Login']['password']
        mainDic['AppDetails'] = []
        for eachPage in eachApp['AppDetails']:
            pageDic = {}
            pageDic['WebPage'] = eachPage['WebPage']
            pageDic['WebPageLinks'] = []
            for eachLink in eachPage['WebPageLinks']:
                linkDic = {}
                if 'method' not in eachLink:
                    eachLink['method'] = "get"
                linkDic['method'] = eachLink['method']
                if 'action' not in eachLink:
                    try:
                        linkDic['href'] = eachLink['href']
                    except:
                        continue
                else:
                    linkDic['action'] = eachLink['action']
                    linkDic['params'] = []
                    if 'params' not in eachLink:
                        eachLink['params'] = []
                    for eachInput in eachLink['params']:
                        inputDic = {}
                        if 'name' not in eachInput:
                            continue
                        else:
                            inputDic['name'] = eachInput['name']
                        if 'type' not in eachInput:
                            eachInput['type'] = 'text'
                        inputDic['type'] = eachInput['type']
                        if 'value' not in eachInput:
                            if eachInput['type'].lower() == 'button':
                                eachInput['value'] = ''
                            elif eachInput['type'].lower() == 'checkbox':
                                eachInput['value'] = ''
                            elif eachInput['type'].lower() == 'color':
                                eachInput['value'] = '#ff0000'
                            elif eachInput['type'].lower() == 'date':
                                eachInput['value'] = '2016-12-12'
                            elif eachInput['type'].lower() == 'datetime':
                                eachInput['value'] = '2016-04-13T01:01'
                            elif eachInput['type'].lower() == 'datetime-local':
                                eachInput['value'] = '2016-04-13T01:01'
                            elif eachInput['type'].lower() == 'email':
                                eachInput['value'] = 'example@ex.com'
                            elif eachInput['type'].lower() == 'file':
                                eachInput['value'] = ''
                            elif eachInput['type'].lower() == 'hidden':
                                eachInput['value'] = 'rand'
                            elif eachInput['type'].lower() == 'image':
                                eachInput['value'] = ''
                            elif eachInput['type'].lower() == 'month':
                                eachInput['value'] = '2016-12'
                            elif eachInput['type'].lower() == 'number':
                                eachInput['value'] = '1'
                            elif eachInput['type'].lower() == 'password':
                                eachInput['value'] = 'password'
                            elif eachInput['type'].lower() == 'radio':
                                eachInput['value'] = ''
                            elif eachInput['type'].lower() == 'range':
                                eachInput['value'] = '1'
                            elif eachInput['type'].lower() == 'reset':
                                eachInput['value'] = ''
                            elif eachInput['type'].lower() == 'search':
                                eachInput['value'] = 'man'
                            elif eachInput['type'].lower() == 'submit':
                                eachInput['value'] = 'Submit'
                            elif eachInput['type'].lower() == 'tel':
                                eachInput['value'] = '1'
                            elif eachInput['type'].lower() == 'text':
                                eachInput['value'] = 'rand'
                            elif eachInput['type'].lower() == 'time':
                                eachInput['value'] = '00:59'
                            elif eachInput['type'].lower() == 'url':
                                eachInput['value'] = 'http://www.google.com'
                            elif eachInput['type'].lower() == 'week':
                                eachInput['value'] = '2016-W14'
                            else:
                                eachInput['value'] = ''
                        inputDic['value'] = eachInput['value']
                        linkDic['params'].append(inputDic)
                pageDic['WebPageLinks'].append(linkDic)
            mainDic['AppDetails'].append(pageDic)
        mainList.append(mainDic)
    if not os.path.exists("Phase2/output/" + appName + "/"):
        os.makedirs("Phase2/output/" + appName + "/")
    with open("Phase2/output/" + appName + "/" + argv, 'w') as outfile:
        json.dump(mainList, outfile)

appName = sys.argv[1]

for file in os.listdir("Phase1/output/" + appName):
    if(file.endswith(".json")):
        main(file,appName)
