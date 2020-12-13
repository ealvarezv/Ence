# $language = "python"
# $interface = "1.0"

# Main function of the script

# ################### IMPORT ####################
import json
import os
import paramiko
import sys
import time
import urllib.request

from scp import SCPClient
from datetime import datetime


# ################### CONSTANTS ####################
OUTPUT_FOLDER = "_output/"

SERVER_PORT = 49738
SERVER_IP = "89.107.49.125"
SERVER_USER = "ence"
SERVER_PASS = "EIVmNP3a5K"


# ################### FUNCTIONS ####################
# Function to know the status of each locator
def getStatus():
    currentTime = time.time()

    currentFolder = os.path.dirname(os.path.abspath(__file__))
    fileName = (currentFolder + "/" + OUTPUT_FOLDER + "/locatorStatus"
                + str(round(currentTime)) + ".csv")
    objFile = open(fileName, "w")

    url = "http://192.168.123.124:9090/qpe/getLocatorInfo?humanReadable=True"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())

    i = 0
    while i < len(data["locators"]):
        timePacket = time.time() * 1000
        locatorName = data["locators"][i]["name"]
        locatorStatus = data["locators"][i]["connection"]
        locatorMode = data["locators"][i]["mode"]
        locatorIP = data["locators"][i]["ipAddress"]
        locatorSensitivity = data["locators"][i]["sensitivity"]

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

        objFile.write("{},{},{},{},{},{},{}\n".format(locatorName, locatorStatus,
                      locatorMode, locatorIP, locatorSensitivity,
                      str(timeLastGoodPacketTS), str(timeLastPacketTS)))
        i += 1

    objFile.close()

    print("[LOG] [getStatus] Analyzed Time: "
          + str(datetime.fromtimestamp(currentTime)))

    return fileName

# Function to create SSH Cliente
def createSSHClient(server, port, user, password):
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, port, user, password)
    return client


# Main Function
def main():
    print("\n#################### START ####################")

    while True:
        ssh = createSSHClient(SERVER_IP, SERVER_PORT, SERVER_USER, SERVER_PASS)
        scp = SCPClient(ssh.get_transport())

        scp.put(getStatus())
        scp.close()
        ssh.close()

        time.sleep(60)

    print("\n#################### GAME OVER ####################\n")


# ################### EJECUCION ####################
# Script execution
main()
