# $language = "python"
# $interface = "1.0"

# Main function of the script

# ################### IMPORT ####################
import json
import os
import paramiko
import socket
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

AP_NUMBER = 21
WLC_IP = "192.168.123.124"
WLC_PORT = 8443
QPE_IP = "192.168.123.124"
QPE_PORT = 9090


# ################### FUNCTIONS ####################
# Function to know the status of each AP
def getAPStatus(currentTime):
    currentFolder = os.path.dirname(os.path.abspath(__file__))
    fileAPName = (currentFolder + "/" + OUTPUT_FOLDER + "/APStatus"
                  + str(round(currentTime)) + ".csv")
    objAPFile = open(fileAPName, "w")

    objAPFile.write("{},{},{}\n".format("AP Name", "AP IP", "AP Status"))
    for i in range(1, AP_NUMBER + 1):
        APName = ("AP-" + str(i))
        ipAddress = ("192.168.123." + str(i))
        response = os.system("ping -c 1 " + ipAddress)
        if response == 0:
            APStatus = "OK"
        else:
            APStatus = "KO"

        objAPFile.write("{},{},{}\n".format(APName, ipAddress, APStatus))

    objAPFile.close()

    print("[LOG] [getAPStatus] Analyzed Time: "
          + str(datetime.fromtimestamp(currentTime)))

    return fileAPName


# Function to know the status of the WLC
def getWLCStatus(currentTime):
    currentFolder = os.path.dirname(os.path.abspath(__file__))
    fileWLCName = (currentFolder + "/" + OUTPUT_FOLDER + "/WLCStatus"
                   + str(round(currentTime)) + ".csv")
    objWLCFile = open(fileWLCName, "w")

    objWLCFile.write("{},{},{}\n".format("WLC IP", "WLC Port", "WLC Status"))

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((WLC_IP, int(WLC_PORT)))
        s.shutdown(2)
        WLCStatus = "OK"
    except Exception:
        WLCStatus = "KO"
    finally:
        s.close()

    objWLCFile.write("{},{},{}\n".format(WLC_IP, WLC_PORT, WLCStatus))
    objWLCFile.close()

    print("[LOG] [getWLCStatus] Analyzed Time: "
          + str(datetime.fromtimestamp(currentTime)))

    return fileWLCName


# Function to know the status of each locator
def getLocatorStatus(currentTime):
    currentFolder = os.path.dirname(os.path.abspath(__file__))
    fileLocatorName = (currentFolder + "/" + OUTPUT_FOLDER + "/locatorStatus"
                       + str(round(currentTime)) + ".csv")
    objLocatorFile = open(fileLocatorName, "w")

    url = "http://192.168.123.124:9090/qpe/getLocatorInfo?humanReadable=True"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())

    objLocatorFile.write("{},{},{},{},{},{},{}\n".format("Locator Name",
                         "Locator Status", "Locator Mode", "Locator IP",
                         "Locator Sensitivity", "timeLastGoodPacketTS",
                         "timeLastPacketTS"))

    if data["code"] == 0:
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

            objLocatorFile.write("{},{},{},{},{},{},{}\n".format(locatorName,
                                 locatorStatus, locatorMode,
                                 locatorIP, locatorSensitivity,
                                 str(timeLastGoodPacketTS), str(timeLastPacketTS)))
            i += 1
    else:
        objLocatorFile.write("Error Code: {}\n".format(data["code"]))

    objLocatorFile.close()

    print("[LOG] [getLocatorStatus] Analyzed Time: "
          + str(datetime.fromtimestamp(currentTime)))

    return fileLocatorName


# Function to know the status of each locator
def getQPEStatus(currentTime):
    currentFolder = os.path.dirname(os.path.abspath(__file__))
    fileQPEName = (currentFolder + "/" + OUTPUT_FOLDER + "/QPEStatus"
                   + str(round(currentTime)) + ".csv")
    objQPEFile = open(fileQPEName, "w")

    objQPEFile.write("{},{},{}\n".format("QPE IP", "QPE Port", "QPE Status"))

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((QPE_IP, int(QPE_PORT)))
        s.shutdown(2)
        QPEStatus = "OK"
    except Exception:
        QPEStatus = "KO"

    objQPEFile.write("{},{},{}\n".format(QPE_IP, QPE_PORT, QPEStatus))
    objQPEFile.close()

    print("[LOG] [getQPEStatus] Analyzed Time: "
          + str(datetime.fromtimestamp(currentTime)))

    return fileQPEName


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
        currentTime = time.time()
        ssh = createSSHClient(SERVER_IP, SERVER_PORT, SERVER_USER, SERVER_PASS)
        scp = SCPClient(ssh.get_transport())

        scp.put(getAPStatus(currentTime))
        scp.put(getWLCStatus(currentTime))
        scp.put(getLocatorStatus(currentTime))
        scp.put(getQPEStatus(currentTime))

        scp.close()
        ssh.close()

        time.sleep(300)

    print("\n#################### GAME OVER ####################\n")


# ################### EXECUTION ####################
# Script execution
main()
