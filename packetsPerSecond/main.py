# $language = "python"
# $interface = "1.0"

# Main function of the script

# ################### IMPORT ####################
import json
import os
import time
import urllib

import matplotlib.animation as animation
import matplotlib.pyplot as plt

from datetime import datetime


# ################### FUNCTIONS ####################
# Function to print the packets per second sequence
def printResult(i, xs, ys, ax, file):
    url = "http://192.168.123.124:9090/qpe/getPEInfo?humanReadable=True"
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    packetsPerSecond = data["positioningEngine"]["packetsPerSecond"]

    currentTime = datetime.fromtimestamp(time.time())

    file.write(str(currentTime) + "," + str(packetsPerSecond) + "\n")

    xs.append(currentTime)
    ys.append(packetsPerSecond)
    ax.clear()
    ax.plot(xs, ys)

    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Test')
    plt.xlabel('Time')
    plt.ylabel('Packets / Second')


# Main Function
def main():
    fig = plt.figure(1)
    ax = fig.add_subplot(1, 1, 1)
    xs = []
    ys = []

    currentTime = datetime.fromtimestamp(time.time())
    currentFolder = os.path.dirname(os.path.abspath(__file__))
    objFile = open(currentFolder + "/_output/PacketsPerSecond"
                   + str(currentTime) + ".txt", "w")

    while True:
        ani = animation.FuncAnimation(fig, printResult,
                                      fargs=(xs, ys, ax, objFile),
                                      interval=1000)
        plt.show()


# ################### EXECUTION ####################
# Ejecucion Script
main()
