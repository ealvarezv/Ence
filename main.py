# $language = "python"
# $interface = "1.0"

# Main function of the script

# ################### IMPORT ####################
import json
import os

import matplotlib.pyplot as plt


# ################### VARS ####################
# Ruta de Ficheros a usar


# Ruta de Carpetas
inputFolder = "_input/"
outputFolder = "_output/"


# ################### FUNCTIONS ####################
# Main Function
def main():
    print("\n#################### START ####################")

    i = 0
    listFile = os.listdir(inputFolder)
    for file in listFile:
        i += 1
        arrayRawPosition = []
        arrayRawAccuracy = []
        arraySmoothedPosition = []
        arraySmoothedAccuracy = []

        modifyJsonFormat(inputFolder, outputFolder, file)

        drawFile = os.path.join(outputFolder, file).replace("log", "png")
        file = os.path.join(outputFolder, file)
        parserFile = json.load(open(file, "r"))

        for register in parserFile:
            arrayRawPosition.append(register["position"])
            arrayRawAccuracy.append(register["positionAccuracy"])
            arraySmoothedPosition.append(register["smoothedPosition"])
            arraySmoothedAccuracy.append(register["smoothedPositionAccuracy"])

        printResult(arrayRawPosition, arrayRawAccuracy, i)
        plt.savefig(drawFile)

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
def printResult(arrayRawPosition, arrayRawAccuracy, location):
    i = 0

    plt.subplot(4, 4, location)
    for position in arrayRawPosition:
        plt.plot(position[0], position[1], createPoint(arrayRawAccuracy, i))
        i += 1

    rawAccuracy = round(sum(arrayRawAccuracy) / len(arrayRawAccuracy), 6)
    smoothedAccuracy = round(sum(arrayRawAccuracy) / len(arrayRawAccuracy), 6)
    plt.title("Raw Accuracy: " + str(rawAccuracy) + " / SmoothedAccuracy: "
              + str(smoothedAccuracy))


# Function to create the point with the correct colour
# 0.00 - 0.50   'g'	green
# 0.50 - 0.75   'y'	yellow
# 0.75 - 1.00   'r'	red
# 1.00 - 1.25   'm'	magenta
# > 1.25        'k'	black
def createPoint(array, position):
    accuracy = array[position]
    if accuracy <= 0.5:
        return("g.")
    elif accuracy <= 0.75:
        return("y.")
    elif accuracy <= 1:
        return("r.")
    elif accuracy <= 1.25:
        return("m.")
    else:
        return("k.")


# ################### EJECUCIÓN ####################
# Ejecución Script
main()
