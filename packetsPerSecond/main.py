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
# Function to print the packets per second sequence
def printResult(i, xs, ys, ax, file):
    url = "http://192.168.123.124:9090/qpe/getPEInfo?humanReadable=True"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())
    packetsPerSecond = data["positioningEngine"]["packetsPerSecond"]

    currentTime = datetime.fromtimestamp(time.time())

    # xs.append(currentTime)
    # ys.append(packetsPerSecond)
    # ax.clear()
    # ax.plot(xs, ys)
    #
    # plt.xticks(rotation=45, ha='right')
    # plt.subplots_adjust(bottom=0.30)
    # plt.title('Test')
    # plt.xlabel('Time')
    # plt.ylabel('Packets / Second')

    file.write(str(currentTime) + "," + str(packetsPerSecond) + "\n")
    file.flush()

    print("[LOG] [printResult] " + str(currentTime) + ": " + str(round(packetsPerSecond,2)) + " pck/s")

# Main Function
def main():
    print("\n#################### START ####################")

    currentTime = time.time()

    currentFolder = os.path.dirname(os.path.abspath(__file__))
    fileName = (currentFolder + "/" + OUTPUT_FOLDER + "/PacketsPerSecond"
                + str(currentTime) + ".txt")
    objFile = open(fileName, "w")

    arrayLocatorFailed = []

    fig = plt.figure(1)
    ax = fig.add_subplot(1, 1, 1)
    xs = []
    ys = []

    while True:
        printResult("0", xs, ys, ax, objFile)
        time.sleep(5)

    # ani = animation.FuncAnimation(fig, printResult,
    #                               fargs=(xs, ys, ax, objFile),
    #                               interval=5000)
    # plt.show()


# ################### EXECUTION ####################
# Ejecucion Script
main()
