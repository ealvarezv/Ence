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

    listFile = os.listdir(inputFolder)
    for file in listFile:
        arrayRawPosition = []
        arrayRawAccuracy = []
        arraySmoothedPosition = []
        arraySmoothedAccuracy = []

        modifyJsonFormat(inputFolder, outputFolder, file)

        file = os.path.join(outputFolder, file)
        parserFile = json.load(open(file, "r"))

        for register in parserFile:
            arrayRawPosition.append(register["position"])
            arrayRawAccuracy.append(register["positionAccuracy"])
            arraySmoothedPosition.append(register["smoothedPosition"])
            arraySmoothedAccuracy.append(register["smoothedPositionAccuracy"])

        printResult(arrayRawPosition, arrayRawAccuracy)

        print(round(sum(arrayRawAccuracy)/len(arrayRawAccuracy), 6))
        print(round(sum(arraySmoothedAccuracy)/len(arraySmoothedAccuracy), 6))
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
def printResult(arrayRawPosition, arrayRawAccuracy):
    print(arrayRawPosition)
    print(arrayRawAccuracy)
    plt.plot(arrayRawPosition, 'bx')

    plt.savefig("hola.png")
    plt.show()


# ################### EJECUCIÓN ####################
# Ejecución Script
main()
