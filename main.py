# $language = "python"
# $interface = "1.0"

# Main function of the script

# ################### IMPORT ####################
import json
import os
import time
import urllib


# ################### CONSTANTS ####################
OUTPUT_FOLDER = "_output/"


# ################### FUNCTIONS ####################
# Function to know the status of each locator
def getStatus(file):
    currentTime = time.time()

    url = "http://192.168.123.124:9090/qpe/getLocatorInfo?humanReadable=True"
    response = urllib.urlopen(url)
    data = json.loads(response.read())

    i = 0
    while i < len(data["locators"]):
        timePacket = time.time() * 1000
        locatorName = data["locators"][i]["name"]
        locatorStatus = data["locators"][i]["connection"]

        if data["locators"][i]["lastGoodPacketTS"] is None:
            locatorLastGoodPacketTS = 0
        else:
            locatorLastGoodPacketTS = data["locators"][i]["lastGoodPacketTS"]

        if data["locators"][i]["lastPacketTS"] is None:
            locatorLastGoodPacketTS = 0
        else:
            locatorLastPacketTS = data["locators"][i]["lastPacketTS"]

        timeLastGoodPacketTS = timePacket - locatorLastGoodPacketTS
        timeLastPacketTS = timePacket - locatorLastPacketTS

        file.write(str(currentTime) + "," + locatorName + "," + locatorStatus
                   + "," + str(timeLastGoodPacketTS) + ","
                   + str(timeLastPacketTS) + "\n")
        i += 1

    file.write("\n")
    print("[LOG] [getStatus] Analyzed Time: " + str(currentTime))


# Main Function
def main():
    print("\n#################### START ####################")

    i = 0
    while True:
        currentTime = time.time()
        currentFolder = os.path.dirname(os.path.abspath(__file__))
        objFile = open(currentFolder + "/" + OUTPUT_FOLDER + "/LocatorStatus"
        + str(currentTime) + ".txt", "w")

        while i < 720:
            getStatus(objFile)
            time.sleep(5)
            i += 1

        printResult(objFile)
        i = 0

    print("\n#################### GAME OVER ####################\n")


# ################### EJECUCION ####################
# Script execution
main()
