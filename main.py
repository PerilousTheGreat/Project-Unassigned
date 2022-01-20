import json
import re
from playsound import playsound
import psutil

from mitmproxy import proxy, options, http
from mitmproxy.tools.dump import DumpMaster
from mitmproxy.addons import core

class AddHeader:

    def __init__ (self, contents):

        self.container = "/trade/"
        self.transfermarket = "/transfermarket?"

        self.boughtContents = contents
        self.block = False

    def request(self, flow: http.HTTPFlow):

        if self.block == True:

            if self.transfermarket in flow.request.pretty_url:
                flow.kill()

    def response(self, flow: http.HTTPFlow):

        if flow.request.method == "PUT":

            if self.container in flow.request.pretty_url:

                if flow.response.status_code == 200:
                        flow_content = flow.response.text
                        res_id = flow_content.split('"resourceId":')[1].split(",")[0]
                        trade_id = flow_content.split('itemData":{"id":')[1].split(",")[0]

                        playerData = AddPlayer(res_id, int(trade_id), self.boughtContents)

                        newJSON = playerData.logPurchase()
                        if newJSON != "Player not found":
                            self.boughtContents = newJSON

                        if playerData.maxPurchase() == True:
                            self.block = True
                            killBrowser("opera.exe")

                elif flow.response.status_code == 521:
                    #Buy Ban
                    playsound("siren.wav")
                    print("Buy Ban")
                    self.block = True

                    killBrowser("opera.exe")


                elif flow.response.status_code == 458:
                    #Captcha
                    playsound("siren.wav")
                    print("Captcha")
                    killBrowser("opera.exe")


                # elif flow.response.status_code == 461:
                #         print("Unsuccessful Purchase")


class AddPlayer():

    def __init__(self, playerID, cardID, contents):

        self.playerID = playerID
        self.tradeID = cardID
        self.boughtContents = contents

        self.maximum = 534

    def logPurchase(self):

        try:
            self.boughtContents[self.playerID]["count"] += 1
            self.boughtContents[self.playerID]["arrayIDs"].append(self.tradeID)

            self.updateJSON()
            self.maxPurchase()

            return self.boughtContents

        except:
            self.boughtContents["unresolved"]["count"] += 1
            self.boughtContents["unresolved"]["arrayIDs"].append(self.tradeID)
            self.boughtContents["unresolved"]["resourceIDs"].append(self.playerID)
            self.updateJSON()
            self.maxPurchase()

            playsound("siren.wav")
            return "Player not found"

    def updateJSON(self):

        with open("bought.json", "w") as file:
            json.dump(self.boughtContents, file, indent=4)

        file.close()

    def maxPurchase(self):

        try:
            if self.boughtContents[self.playerID]["count"] == self.maximum:

                playsound("ding.mp3")
                return True
        except:
            return False

def start(boughtContents):
    myaddon = AddHeader(boughtContents)
    opts = options.Options(listen_host='127.0.0.1', listen_port=8080, allow_hosts=["utas.external.s2.fut.ea.com"])
    pconf = proxy.config.ProxyConfig(opts)
    m = DumpMaster(opts)
    m.server = proxy.server.ProxyServer(pconf)
    m.addons.add(myaddon)

    try:
        m.run()
    except KeyboardInterrupt:
        m.shutdown()

def killBrowser(browserName):

    for proc in psutil.process_iter():
    # check whether the process name matches
        if proc.name() == browserName:
            proc.kill()


# def playerName(resourceID, fileContents):
#
#     for i in fileContents:
#         if i == resourceID:
#             return fileContents[i]
#
#     return "Not Found"



if __name__ == "__main__":

    file = open("bought.json", "r")
    contents = json.load(file)
    file.close()

    start(contents)
