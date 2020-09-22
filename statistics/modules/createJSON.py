# $language = "python"
# $interface = "1.0"

# Module createJSON.py

# ################### IMPORT ####################
import os

from threading import Thread


# ################### CONSTANTS ####################


# ################### FUNCTIONS ####################
# Function to modify the JSON File from Quuppa
def createJSON(inputFolder, tempFolder, outputFolder):
    print("\n##### modifyFile #####")
    listFile = os.listdir(inputFolder)
    threads = []

    for file in listFile:
        fileContent = file.split("_")
        drawFileName = ("EnceHUV_" + fileContent[3]
                        + fileContent[4].replace(".log", "") + "_"
                        + fileContent[1])
        drawFile = outputFolder + drawFileName + ".png"

        if os.path.isfile(drawFile):
            print("[LOG] [createJSON]" + drawFileName + " Already Created")
        else:
            process = Thread(target=modifyJsonFormat, args=[inputFolder,
                             tempFolder, file])
            process.start()
            threads.append(process)

    for process in threads:
        process.join()
    print("modifyFile Finished")


# Function to modify the JSON File from Quuppa
def modifyJsonFormat(inputFolder, outputFolder, file):
    initialFile = os.path.join(inputFolder, file)
    objFile = open(initialFile, "r").read().splitlines()
    finalFile = os.path.join(outputFolder, file)
    objFinalFile = open(finalFile, "w")

    j = 0
    objFinalFile.write("[" + "\n")
    for line in objFile:
        j += 1
        if line == "}":
            numLine = j

    i = 0
    endFile = False
    for line in objFile:
        i += 1
        if line == "}":
            if i == len(objFile):
                line = "}" + "\n"
            elif i == numLine:
                line = "}" + "\n"
                endFile = True
            else:
                line = "}," + "\n"
        elif endFile:
            line = ""
        elif "#" in line:
            line = ""
        else:
            line = line + "\n"
        objFinalFile.write(line)

    objFinalFile.write("]")
    objFinalFile.close()
    print("[LOG] [modifyJsonFormat]" + file + " Modified")
