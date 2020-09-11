# $language = "python"
# $interface = "1.0"

# Module functions.py

# ################### IMPORT ####################
import json
import math
import matplotlib.pyplot as plt
import os
import queue
import shutil
import timeit


from threading import Thread

# # ################### CONSTANTS ####################
from modules._constants import OUTPUT_FOLDER, THRESHOLD_LEVEL1, THRESHOLD_LEVEL2,\
    THRESHOLD_LEVEL3, THRESHOLD_LEVEL4, COLOR_LEVEL1, COLOR_LEVEL2,\
    COLOR_LEVEL3, COLOR_LEVEL4, COLOR_LEVEL5, PLOT_X, PLOT_Y, NUM_COLUMNS,\
    FONT_SIZE, MARKER

from modules.pixel_accuracy import grid_maker


# ################### FUNCTIONS ####################
# Function to create the structure for files
def createStructure(folder1, folder2):
    print("\n##### createStructure #####")
    createFolder(folder1)
    createFolder(folder2)


# Function to create a folder
def createFolder(folder):
    if not os.path.exists(folder):
        os.mkdir(folder)
        print("Folder " + folder + " created")


# Function to modify the JSON File from Quuppa
def modifyFile(inputFolder, tempFolder):
    print("\n##### modifyFile #####")
    listFile = os.listdir(inputFolder)
    threads = []

    for file in listFile:
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
    print(file + " Modified")


# Function to process the files
def processFile(tempFolder, outputFolder):
    print("\n##### processFile #####")
    listFile = os.listdir(tempFolder)
    numRow = math.ceil(len(listFile)/NUM_COLUMNS)
    queueResult = queue.Queue()
    threads = []
    numFile = 0

    for file in listFile:
        t = timeit.default_timer()
        fileContent = file.split("_")
        drawFileName = ("EnceHUV_" + fileContent[1] + "_" + fileContent[3]
                        + fileContent[4].replace(".log", ""))
        drawFile = outputFolder + drawFileName + ".png"
        if os.path.isfile(drawFile):
            print(drawFileName + " Already Created / Time "
                  + str(round((timeit.default_timer()-t), 2)))
        else:
            numFile += 1
            process = Thread(target=processJSONFile, args=[tempFolder, file,
                             numFile, queueResult, drawFileName])
            process.start()
            threads.append(process)

    for process in threads:
        process.join()

    queueResultArray = []
    while True:
        if not queueResult.empty():
            queueResultArray.append(queueResult.get())
        else:
            break

    print("Data obtained")
    paintResult(queueResultArray, numRow, outputFolder)


# Function to process the JSON files
def processJSONFile(folder, file, numFile, queue, drawFileName):
    arrayTag = []
    filePath = os.path.join(folder, file)
    parserFile = json.load(open(filePath, "r"))

    for register in parserFile:
        if register["name"] not in arrayTag:
            arrayTag.append(register["name"])

    arrayPixel = []
    arrayRawPosition = []
    arrayRawAccuracy = []
    arrayRawColorPoint = []
    arraySmoothedPosition = []
    arraySmoothedAccuracy = []
    arraySmoothedColorPoint = []

    for register in parserFile:
        arrayPixelInfo = []
        arrayPixelInfo.append(register["position"][0])
        arrayPixelInfo.append(register["position"][1])
        arrayPixelInfo.append(register["positionAccuracy"])

        arrayPixel.append(arrayPixelInfo)
        arrayRawPosition.append(register["position"])
        arrayRawAccuracy.append(register["positionAccuracy"])
        arrayRawColorPoint.append(colorPoint(
            register["positionAccuracy"]))
        arraySmoothedPosition.append(register["smoothedPosition"])
        arraySmoothedAccuracy.append(
            register["smoothedPositionAccuracy"])
        arraySmoothedColorPoint.append(colorPoint(
            register["smoothedPositionAccuracy"]))

    allTags = True
    drawFileNameTag = drawFileName + ".png"
    rawLevelAccuracy = calculateLevelAccuracy(arrayRawAccuracy)
    smoothedLevelAccuracy = calculateLevelAccuracy(arraySmoothedAccuracy)
    if len(arrayRawAccuracy) == 0:
        rawTotalAccuracy = 0
    else:
        rawTotalAccuracy = round(sum(arrayRawAccuracy)
                                 / len(arrayRawAccuracy), 3)
        if len(arraySmoothedAccuracy) == 0:
            smoothedTotalAccuracy = 0
        else:
            smoothedTotalAccuracy = round(sum(arraySmoothedAccuracy)
                                          / len(arraySmoothedAccuracy), 3)
    queue.put([arrayRawPosition, arrayRawAccuracy, arrayRawColorPoint,
              rawTotalAccuracy, rawLevelAccuracy, arraySmoothedPosition,
              arraySmoothedAccuracy, smoothedTotalAccuracy,
              smoothedLevelAccuracy, file, numFile, drawFileNameTag,
              allTags, arrayPixel])

    for tag in arrayTag:
        arrayPixel = []
        arrayRawPosition = []
        arrayRawAccuracy = []
        arrayRawColorPoint = []
        arraySmoothedPosition = []
        arraySmoothedAccuracy = []
        arraySmoothedColorPoint = []

        for register in parserFile:
            if register["name"] == tag:
                arrayPixelInfo = []
                arrayPixelInfo.append(register["position"][0])
                arrayPixelInfo.append(register["position"][1])
                arrayPixelInfo.append(register["positionAccuracy"])

                arrayPixel.append(arrayPixelInfo)
                arrayRawPosition.append(register["position"])
                arrayRawAccuracy.append(register["positionAccuracy"])
                arrayRawColorPoint.append(colorPoint(
                    register["positionAccuracy"]))
                arraySmoothedPosition.append(register["smoothedPosition"])
                arraySmoothedAccuracy.append(
                    register["smoothedPositionAccuracy"])
                arraySmoothedColorPoint.append(colorPoint(
                    register["smoothedPositionAccuracy"]))

        allTags = False
        drawFileNameTag = drawFileName + "_" + tag + ".png"
        rawLevelAccuracy = calculateLevelAccuracy(arrayRawAccuracy)
        smoothedLevelAccuracy = calculateLevelAccuracy(arraySmoothedAccuracy)
        if len(arrayRawAccuracy) == 0:
            rawTotalAccuracy = 0
        else:
            rawTotalAccuracy = round(sum(arrayRawAccuracy)
                                     / len(arrayRawAccuracy), 3)
        if len(arraySmoothedAccuracy) == 0:
            smoothedTotalAccuracy = 0
        else:
            smoothedTotalAccuracy = round(sum(arraySmoothedAccuracy)
                                          / len(arraySmoothedAccuracy), 3)

        queue.put([arrayRawPosition, arrayRawAccuracy, arrayRawColorPoint,
                  rawTotalAccuracy, rawLevelAccuracy, arraySmoothedPosition,
                  arraySmoothedAccuracy, smoothedTotalAccuracy,
                  smoothedLevelAccuracy, file, numFile, drawFileNameTag,
                  allTags, arrayPixel])


# Function to paint the results in a matplot
def paintResult(queue, numRow, outputFolder):
    for result in queue:
        t = timeit.default_timer()
        printResult(result[0], result[2], result[3], result[4], result[9],
                    result[10], outputFolder, result[11], result[12])
        print(result[11] + " Created / Time "
              + str(round((timeit.default_timer()-t), 2)))

        plot_accuracy(grid_maker(data=result[13]), result[3], outputFolder,
                      result[11], result[12])


# Function to print the results in a graph
def printResult(arrayPosition, arrayColor, totalAccuracy, levelAccuracy, file,
                numFile, outputFolder, drawFileName, allTags):
    i = 0
    for position in arrayPosition:
        plt.plot(position[0], position[1], color=arrayColor[i], marker=MARKER)
        i += 1

    plt.xlim(PLOT_X)
    plt.ylim(PLOT_Y)
    plt.axis('off')
    plt.title(drawFileName.replace(".png", "")
              + "\nAccuracy : " + str(totalAccuracy))

    texts = ["Level 1", "Level 2", "Level 3", "Level 4", "Level 5"]
    colors = [COLOR_LEVEL1, COLOR_LEVEL2, COLOR_LEVEL3, COLOR_LEVEL4,
              COLOR_LEVEL5]
    legendPatches = [plt.plot([], [], marker="o", ms=5, ls="", mec=None,
                     color=colors[i])[0]
                     for i in range(len(texts))]
    plt.legend(legendPatches, levelAccuracy, loc="lower right", frameon=False,
               fontsize=FONT_SIZE)

    varsDrawFolder = drawFileName.split("_")
    if allTags:
        drawFolder = OUTPUT_FOLDER
    else:
        drawFolder = (OUTPUT_FOLDER + varsDrawFolder[0] + "_"
                      + varsDrawFolder[1] + "_" + varsDrawFolder[2] + "/")
        createFolder(drawFolder)

    plt.savefig((drawFolder + drawFileName), dpi=200)
    plt.clf()


def plot_accuracy(array, totalAccuracy, outputFolder, drawFileName, allTags):
    x = 0
    y = 0

    lenArray = len(array)
    for yPosition in array:
        for xPosition in yPosition:
            plt.plot(x, (lenArray - y), color=colorPoint(array[y][x]),
                     marker="s")
            x += 1
        y += 1
        x = 0

    plt.axis('off')
    plt.title(drawFileName.replace(".png", "")
              + "\nAccuracy : " + str(totalAccuracy))

    varsDrawFolder = drawFileName.split("_")
    if allTags:
        drawFolder = OUTPUT_FOLDER
    else:
        drawFolder = (OUTPUT_FOLDER + varsDrawFolder[0] + "_"
                      + varsDrawFolder[1] + "_" + varsDrawFolder[2] + "/")

    plt.savefig((drawFolder + "Pixel_" + drawFileName), dpi=200)
    plt.clf()


# Function to create the point with the correct colour
def colorPoint(value):
    if value == 0:
        return("w")
    if value <= THRESHOLD_LEVEL1:
        return(COLOR_LEVEL1)
    elif value <= THRESHOLD_LEVEL2:
        return(COLOR_LEVEL2)
    elif value <= THRESHOLD_LEVEL3:
        return(COLOR_LEVEL3)
    elif value <= THRESHOLD_LEVEL4:
        return(COLOR_LEVEL4)
    else:
        return(COLOR_LEVEL5)


# Function to calculate statistics
def calculateLevelAccuracy(arrayRawAccuracy):
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

    if len(arrayRawAccuracy) == 0:
        numLevel1Percent = 0
    else:
        numLevel1Percent = ("[0-" + str(THRESHOLD_LEVEL1) + "]: "
                            + str(round(numLevel1 / len(arrayRawAccuracy)
                                  * 100, 2)) + "%")

    if len(arrayRawAccuracy) == 0:
        numLevel2Percent = 0
    else:
        numLevel2Percent = ("[" + str(THRESHOLD_LEVEL1) + "-"
                            + str(THRESHOLD_LEVEL2) + "]: "
                            + str(round(numLevel2 / len(arrayRawAccuracy)
                                  * 100, 2)) + "%")

    if len(arrayRawAccuracy) == 0:
        numLevel3Percent = 0
    else:
        numLevel3Percent = ("[" + str(THRESHOLD_LEVEL2) + "-"
                            + str(THRESHOLD_LEVEL3) + "]: "
                            + str(round(numLevel3 / len(arrayRawAccuracy)
                                  * 100, 2)) + "%")

    if len(arrayRawAccuracy) == 0:
        numLevel4Percent = 0
    else:
        numLevel4Percent = ("[" + str(THRESHOLD_LEVEL3) + "-"
                            + str(THRESHOLD_LEVEL4) + "]: "
                            + str(round(numLevel4 / len(arrayRawAccuracy)
                                  * 100, 2)) + "%")

    if len(arrayRawAccuracy) == 0:
        numLevel5Percent = 0
    else:
        numLevel5Percent = (">" + str(THRESHOLD_LEVEL4) + ": "
                            + str(round(numLevel5 / len(arrayRawAccuracy)
                                  * 100, 2)) + "%")

    return [numLevel1Percent, numLevel2Percent, numLevel3Percent,
            numLevel4Percent, numLevel5Percent]


# Function to delete the structure for temporal files
def deleteStructure(srcFolder, dstFolder):
    print("\n##### deleteTempStructure #####")
    if os.path.exists(srcFolder):
        listFile = os.listdir(srcFolder)
        for file in listFile:
            src = srcFolder + file
            dst = dstFolder + file
            shutil.move(src, dst)
        print("Files moved from " + srcFolder + " to " + dstFolder)
        os.rmdir(srcFolder)
        print("Folder " + srcFolder + " deleted")
