from mitmproxy import proxy, options, http, ctx
from mitmproxy.tools.dump import DumpMaster
from mitmproxy.addons import core

import json
import requests
import urllib3
import time
import random

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# class AddHeader():
#
#     def __init__(self, sid):
#
#         self.sbcURL = "https://utas.external.s2.fut.ea.com/ut/game/fifa22/sbs/challenge/1289/squad"
#         self.sid = sid
#
#         file = open("bought.json", "r")
#         self.contents = json.load(file)
#         file.close()
#
#     def response(flow: http.HTTPFlow):
#
#         if flow.request.pretty_url == self.sbcURL:
#
#             if flow.response.status_code == 200:
#
#                 clubSender(self.contents, self.sid)
#
#
# def start(sid):
#     myaddon = AddHeader(sid)
#     opts = options.Options(listen_host='127.0.0.1', listen_port=8080, allow_hosts=["utas.external.s2.fut.ea.com"])
#     pconf = proxy.config.ProxyConfig(opts)
#     m = DumpMaster(opts)
#     m.server = proxy.server.ProxyServer(pconf)
#     m.addons.add(myaddon)
#
#     try:
#         m.run()
#     except KeyboardInterrupt:
#         m.shutdown()

def get_contents(dictObject, n):
    y = 0
    for i in dictObject:
        if y == n:
            return i
        else:
            y += 1

def moveToClub(cardID, headers):

    url = 'https://utas.external.s2.fut.ea.com/ut/game/fifa22/item'
    payload = {"itemData":[{"id":str(cardID),"pile":"club"}]}
    payload = json.dumps(payload)

    response = requests.put(url=url, headers=headers, data=payload, verify=False)
    res_content = response.text

    if '"success":true' in res_content:
        print("Moved player to the club succesfully.")
        return True

    elif "duplicate" in res_content:
        print("Duplicate item exists.")
        return False

    elif '"success":false' in res_content:
        print("Error while attempting to move player.")
        return False


def clubSender(contents, sid):

    headers = {
        'Host': 'utas.external.s2.fut.ea.com',
        'Connection': 'keep-alive',
        'sec-ch-ua': '"Chromium";v="96", "Opera GX";v="82", ";Not A Brand";v="99"',
        'Content-length': '0',
        'X-UT-SID': sid,
        'Content-Type': 'application/json',
        'sec-ch-ua-mobile': '?0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 OPR/82.0.4227.50',
        'sec-ch-ua-platform': '"Windows"',
        'Accept': '*/*',
        'Origin': 'https://www.ea.com',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.ea.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8'
    }

    cards = []

    for i in range(0, len(contents)-1):

        index_contents = get_contents(contents, i)
        #Holds key of the desired index e.g. 139068 (Nani)

        tbs = contents[index_contents]["arrayIDs"][-1]
        #tbs = CARD ID TO BE SENT

        move_result = moveToClub(tbs, headers)

        if (move_result == True):
            del contents[index_contents]["arrayIDs"][-1]
            contents[index_contents]["count"] -= 1

            cards.append(tbs)

            with open("bought.json", "w") as file:
                json.dump(contents, file, indent=4)


        time.sleep(random.randint(1,2))

    if len(cards) == 11:
        result = putSBC(cards, sid)

        if result == True:
            return True

def putSBC(cardContent, sid):

   postHeaders = {

   'Host': 'utas.external.s2.fut.ea.com',
   'Connection': 'keep-alive',
   'sec-ch-ua': '"Chromium";v="96", "Opera GX";v="82", ";Not A Brand";v="99"',
   'X-UT-SID': sid,
   'Content-Type': 'application/json',
   'sec-ch-ua-mobile': '?0',
   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 OPR/82.0.4227.50',
   'sec-ch-ua-platform': '"Windows"',
   'Origin': 'https://www.ea.com',
   'Sec-Fetch-Site': 'same-site',
   'Sec-Fetch-Mode': 'cors',
   'Sec-Fetch-Dest': 'empty',
   'Referer': 'https://www.ea.com/',
   'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8'
   }

   time.sleep(random.randint(7,8))

   post_url = "https://utas.external.s2.fut.ea.com/ut/game/fifa22/sbs/challenge/1289"
   squad_url = "https://utas.external.s2.fut.ea.com/ut/game/fifa22/sbs/challenge/1289/squad"
   sbc_url = "https://utas.external.s2.fut.ea.com/ut/game/fifa22/sbs/challenge/1289?skipUserSquadValidation=false"

   falseStr = "false"
   falseStr = falseStr.strip('"')

   payload = {"players":[{"index":0,"itemData":{"id":cardContent[9],"dream":falseStr}},{"index":1,"itemData":{"id":cardContent[7],"dream":falseStr}},{"index":2,"itemData":{"id":cardContent[10],"dream":falseStr}},{"index":3,"itemData":{"id":cardContent[2],"dream":falseStr}},{"index":4,"itemData":{"id":cardContent[8],"dream":falseStr}},{"index":5,"itemData":{"id":cardContent[6],"dream":falseStr}},{"index":6,"itemData":{"id":cardContent[4],"dream":falseStr}},{"index":7,"itemData":{"id":cardContent[3],"dream":falseStr}},{"index":8,"itemData":{"id":cardContent[0],"dream":falseStr}},{"index":9,"itemData":{"id":cardContent[5],"dream":falseStr}},{"index":10,"itemData":{"id":cardContent[1],"dream":falseStr}},{"index":11,"itemData":{"id":0,"dream":falseStr}},{"index":12,"itemData":{"id":0,"dream":falseStr}},{"index":13,"itemData":{"id":0,"dream":falseStr}},{"index":14,"itemData":{"id":0,"dream":falseStr}},{"index":15,"itemData":{"id":0,"dream":falseStr}},{"index":16,"itemData":{"id":0,"dream":falseStr}},{"index":17,"itemData":{"id":0,"dream":falseStr}},{"index":18,"itemData":{"id":0,"dream":falseStr}},{"index":19,"itemData":{"id":0,"dream":falseStr}},{"index":20,"itemData":{"id":0,"dream":falseStr}},{"index":21,"itemData":{"id":0,"dream":falseStr}},{"index":22,"itemData":{"id":0,"dream":falseStr}}]}

   payload = json.dumps(payload)

   first = requests.post(url=post_url, headers=postHeaders, data=None, verify=False)
   second = requests.put(url=squad_url, headers=postHeaders, data=payload, verify=False)
   third = requests.put(url=sbc_url, headers=postHeaders, verify=False)

   if third.status_code == 200:
       print("SBC success.")
       return True
   else:
       print("SBC error.")


def overrwrite(data):
    with open("completed.json", "w+") as export:
            json.dump(data, export)

            export.close()

file = open("bought.json", "r")
contents = json.load(file)
file.close()

completedFile = open("completed.json", "r+")
completeContents = json.load(completedFile)
completedFile.close()

print("Currently Complete: " + str(completeContents["completed"]))

sid = input("Enter the active session ID: ")
ongoing = True

while ongoing == True:

    result = clubSender(contents, sid)
    if result == True:
        completeContents["completed"] += 1
        overrwrite(completeContents)

        completeNum = completeContents["completed"]
        print(f"Total Successful SBCs: {completeNum}")

    print("")
    decision = input("Want to try another? ")

    if decision != "y":
        ongoing = False
