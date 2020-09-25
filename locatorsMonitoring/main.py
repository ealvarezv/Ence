# $language = "python"
# $interface = "1.0"

# Main function of the script

# ################### IMPORT ####################
import json
import os
import time
import smtplib
import ssl
import urllib.request

import matplotlib.animation as animation
import matplotlib.pyplot as plt

from datetime import datetime
from email.mime.text import MIMEText


# ################### CONSTANTS ####################
OUTPUT_FOLDER = "_output/"

MAIL_PORT = 465
MAIL_SERVER = "smtp.gmail.com"
MAIL_USER = "enriqueavtest@gmail.com"
MAIL_PASS = "anonymous1!"


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

        analyzeResult(locatorName, locatorStatus, currentTime, array)

        file.write(str(datetime.fromtimestamp(currentTime)) + "," + locatorName + "," + locatorStatus
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
            sendAlarm(name, status, datetime.fromtimestamp(time))
    else:
        if status != "ok":
            array.append(name)
            sendAlarm(name, status, datetime.fromtimestamp(time))


def sendAlarm(name, status, time):
    sender = "Onesite Motion Worker <enriqueavtest@gmail.com>"
    receiver = "enrique.alvarez.villace@gmail.com"
    message = f"""
        Site: Ence HUV
        Locator: {name}
        Status: {status}
        Timestamp: {time}"""
    message = MIMEText(message)
    message["From"] = "Onesite Motion Worker <from@smtp.mailtrap.io>"
    message["To"] = "enrique.alvarez.villace@gmail.com"

    if status == "ok":
        message["Subject"] = ("Ence HUV: Up Alarm: " + name + " / " + status)
        print("Up Alarm: " + name + " / " + status + " / " + str(time))
    else:
        message["Subject"] = ("Ence HUV: Down Alarm: " + name + " / " + status)
        print("Down Alarm: " + name + " / " + status + " / " + str(time))

    try:
        with smtplib.SMTP_SSL(MAIL_SERVER, MAIL_PORT) as server:
            # server.set_debuglevel(1)
            server.login(MAIL_USER, MAIL_PASS)
            server.sendmail(sender, receiver, message.as_string())
            server.close()
            print('Sent')
    except smtplib.SMTPServerDisconnected:
        print('Failed to connect to the server. Wrong user/password?')
    except smtplib.SMTPException as e:
        print('SMTP error occurred: ' + str(e))
    except Exception as e:
        print('everything else' + str(e))

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
        time.sleep(5)

        # ani = animation.FuncAnimation(fig, getStatus, fargs=(xs, ys, ax,
        #                             arrayLocatorFailed, objFile), interval=5000)
        #
        # plt.show()

    print("\n#################### GAME OVER ####################\n")


# ################### EJECUCIÓN ####################
# Script execution
main()
