# $language = "python"
# $interface = "1.0"

# Main function of the script

# ################### IMPORT ####################
import json
import os
import time
import urllib.request

import matplotlib.animation as animation
import matplotlib.pyplot as plt

from datetime import datetime


# ################### CONSTANTS ####################
OUTPUT_FOLDER = "_output/"


# ################### FUNCTIONS ####################
# Function to know the status of each locator
def getStatus(i, xs, ys, ax, array, file):
    currentTime = time.time()

    url = "http://192.168.123.124:9090/qpe/getLocatorInfo?humanReadable=True"
    response = urllib.request.urlopen(url)
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

        analyzeResult(locatorName, locatorStatus, timePacket, array)

        file.write(str(currentTime) + "," + locatorName + "," + locatorStatus
                   + "," + str(timeLastGoodPacketTS) + ","
                   + str(timeLastPacketTS) + "\n")
        i += 1


    file.write("\n")

    # xs.append(datetime.fromtimestamp(currentTime))
    # ys.append("")
    # ax.clear()
    # ax.plot(xs, ys)
    #
    # plt.xticks(rotation=45, ha='right')
    # plt.subplots_adjust(bottom=0.30)
    # plt.title('Test')
    # plt.xlabel('Time')
    # plt.ylabel('Packets / Second')

    print("[LOG] [getStatus] Analyzed Time: " + str(datetime.fromtimestamp(currentTime)))


# Function to print the result
def analyzeResult(name, status, time, array):
    if name in array:
        if status == "ok":
            array.remove(name)
            sendAlarm(name, status, time)
    else:
        if status != "ok":
            array.append(name)
            sendAlarm(name, status, time)


def sendAlarm(name, status, time):
    if status == "ok":
        print("Up Alarm: " + name + " / " + status + " / " + str(time))
    else:
        print("Down Alarm: " + name + " / " + status + " / " + str(time))


# Main Function
def main():
    print("\n#################### START ####################")

    currentTime = time.time()

    currentFolder = os.path.dirname(os.path.abspath(__file__))
    fileName = (currentFolder + "/" + OUTPUT_FOLDER + "/LocatorStatus"
                + str(currentTime) + ".txt")
    objFile = open(fileName, "w")

    arrayLocatorFailed = []

    fig = plt.figure(1)
    ax = fig.add_subplot(1, 1, 1)
    xs = []
    ys = []

    while True:
        getStatus ("0", xs, ys, ax, arrayLocatorFailed, objFile)
        time.sleep(10)

        # ani = animation.FuncAnimation(fig, getStatus, fargs=(xs, ys, ax,
        #                             arrayLocatorFailed, objFile), interval=5000)
        #
        # plt.show()

    print("\n#################### GAME OVER ####################\n")


# ################### EJECUCIÓN ####################
# Script execution
main()
