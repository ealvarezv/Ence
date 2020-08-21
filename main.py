# $language = "python"
# $interface = "1.0"

# Main function of the script

# ################### IMPORT ####################
import json
import math
import os

import matplotlib.pyplot as plt


# ################### VARS ####################
# Ruta de Carpetas
inputFolder = "_input/"
outputFolder = "_output/"


# ################### CONSTANTS ####################
THRESHOLD_LEVEL1 = 0.5
THRESHOLD_LEVEL2 = 0.75
THRESHOLD_LEVEL3 = 1
THRESHOLD_LEVEL4 = 1.25

COLOR_LEVEL1 = "#3c783c"
COLOR_LEVEL2 = "#3c783c80"
COLOR_LEVEL3 = "#ffbe00"
COLOR_LEVEL4 = "#c0000080"
COLOR_LEVEL5 = "#c00000"

MARKER = "o"


# ################### FUNCTIONS ####################
# Main Function
def main():
    print("\n#################### START ####################")

    i = 0
    listFile = os.listdir(inputFolder)
    numRow = math.ceil(len(listFile)/2)
    plt.rc("font", size=6)
    for file in listFile:
        i += 1
        arrayRawPosition = []
        arrayRawAccuracy = []
        arraySmoothedPosition = []
        arraySmoothedAccuracy = []

        modifyJsonFormat(inputFolder, outputFolder, file)

        filePath = os.path.join(outputFolder, file)
        parserFile = json.load(open(filePath, "r"))

        for register in parserFile:
            arrayRawPosition.append(register["position"])
            arrayRawAccuracy.append(register["positionAccuracy"])
            arraySmoothedPosition.append(register["smoothedPosition"])
            arraySmoothedAccuracy.append(register["smoothedPositionAccuracy"])

        plt.subplot(numRow, 3, i)
        printResult(arrayRawPosition, arrayRawAccuracy, arraySmoothedPosition,
                    arraySmoothedAccuracy, file)

    plt.savefig("_output/Final_" + file.split("_")[4] + "_"
                + file.split("_")[5].replace(".log", "") + ".png")
    plt.show()

    print("\n#################### GAME OVER ####################\n\n")


# Function to modify the JSON File from Quuppa
def modifyJsonFormat(inputFolder, outputFolder, file):
    initialFile = os.path.join(inputFolder, file)
    objFile = open(initialFile, "r").read().splitlines()
    finalFile = os.path.join(outputFolder, file)
    objFinalFile = open(finalFile, "w")
    i = 0

    objFinalFile.write("[" + "\n")
    for line in objFile:
        i += 1
        if line == "}":
            if i == len(objFile):
                line = "}" + "\n"
            else:
                line = "}," + "\n"
        elif "#" in line:
            line = ""
        else:
            line = line + "\n"
        objFinalFile.write(line)
    objFinalFile.write("]")

    objFinalFile.close()


# Function to print the results in a graph
def printResult(arrayRawPosition, arrayRawAccuracy, arraySmoothedPosition,
                arraySmoothedAccuracy, file):
    i = 0

    for position in arrayRawPosition:
        plt.plot(position[0], position[1], marker=MARKER,
                 color=createPoint(arrayRawAccuracy, i))
        i += 1

    rawAccuracy = round(sum(arrayRawAccuracy) / len(arrayRawAccuracy), 3)
    smoothedAccuracy = round(sum(arraySmoothedAccuracy)
                             / len(arraySmoothedAccuracy), 3)
    plt.title(file.split("_")[1] + "_" + file.split("_")[2]
              + "\nRaw Accuracy: " + str(rawAccuracy)
              + " / Smoothed Accuracy: " + str(smoothedAccuracy))

    texts = ["Level 1", "Level 2", "Level 3", "Level 4", "Level 5"]
    colors = [COLOR_LEVEL1, COLOR_LEVEL2, COLOR_LEVEL3, COLOR_LEVEL4,
              COLOR_LEVEL5]
    legendPatches = [plt.plot([], [], marker=MARKER, ms=5, ls="", mec=None,
                     color=colors[i], label=(calculateStatistics(
                                             arrayRawAccuracy)[i]) + " %")[0]
                     for i in range(len(texts))]
    plt.legend(handles=legendPatches, loc="lower right")


# Function to create the point with the correct colour
def createPoint(array, position):
    accuracy = array[position]
    if accuracy <= THRESHOLD_LEVEL1:
        return(COLOR_LEVEL1)
    elif accuracy <= THRESHOLD_LEVEL2:
        return(COLOR_LEVEL2)
    elif accuracy <= THRESHOLD_LEVEL3:
        return(COLOR_LEVEL3)
    elif accuracy <= THRESHOLD_LEVEL4:
        return(COLOR_LEVEL4)
    else:
        return(COLOR_LEVEL5)


# Function to calculate statistics
def calculateStatistics(arrayRawAccuracy):
    numLevel1 = 0
    numLevel2 = 0
    numLevel3 = 0
    numLevel4 = 0
    numLevel5 = 0

    for accuracy in arrayRawAccuracy:
        if accuracy <= THRESHOLD_LEVEL1:
            numLevel1 += 1
        elif accuracy <= THRESHOLD_LEVEL2:
            numLevel2 += 1
        elif accuracy <= THRESHOLD_LEVEL3:
            numLevel3 += 1
        elif accuracy <= THRESHOLD_LEVEL4:
            numLevel4 += 1
        else:
            numLevel5 += 1

    numLevel1Percent = str(round(numLevel1 / len(arrayRawAccuracy) * 100, 2))
    numLevel2Percent = str(round(numLevel2 / len(arrayRawAccuracy) * 100, 2))
    numLevel3Percent = str(round(numLevel3 / len(arrayRawAccuracy) * 100, 2))
    numLevel4Percent = str(round(numLevel4 / len(arrayRawAccuracy) * 100, 2))
    numLevel5Percent = str(round(numLevel5 / len(arrayRawAccuracy) * 100, 2))

    return [numLevel1Percent, numLevel2Percent, numLevel3Percent,
            numLevel4Percent, numLevel5Percent]


# ################### EJECUCIÓN ####################
# Ejecución Script
main()
