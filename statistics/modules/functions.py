# $language = "python"
# $interface = "1.0"

# Module functions.py

# ################### IMPORT ####################
import json
import math
import matplotlib.pyplot as plt
import numpy as np
import os
import queue
import timeit

from threading import Thread

from modules.structure import createFolder
from modules.utils import read_json, areas_ENCE


# ################### CONSTANTS ####################
from modules._constants import OUTPUT_FOLDER, ACCURACY_THRESHOLD_LEVEL1, ACCURACY_THRESHOLD_LEVEL2,\
    ACCURACY_THRESHOLD_LEVEL3, ACCURACY_THRESHOLD_LEVEL4, ACCURACY_COLOR_LEVEL1, ACCURACY_COLOR_LEVEL2,\
    ACCURACY_COLOR_LEVEL3, ACCURACY_COLOR_LEVEL4, ACCURACY_COLOR_LEVEL5, LATENCY_THRESHOLD_LEVEL1, LATENCY_THRESHOLD_LEVEL2,\
    LATENCY_THRESHOLD_LEVEL3, LATENCY_THRESHOLD_LEVEL4, LATENCY_COLOR_LEVEL1, LATENCY_COLOR_LEVEL2,\
    LATENCY_COLOR_LEVEL3, LATENCY_COLOR_LEVEL4, LATENCY_COLOR_LEVEL5, PLOT_X, PLOT_Y, NUM_COLUMNS,\
    FONT_SIZE, MARKER


# ################### FUNCTIONS ####################
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
        drawFileName = ("EnceHUV_" + fileContent[3]
                        + fileContent[4].replace(".log", "") + "_"
                        + fileContent[1])

        drawFile = outputFolder + drawFileName + ".png"
        if os.path.isfile(drawFile):
            print("[LOG] [processFile]" + drawFileName
                  + " Already Created / Time: "
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

    print("[LOG] [processFile] obtained")
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
    arrayRawColor = []
    arraySmoothedPosition = []
    arraySmoothedAccuracy = []
    arraySmoothedColorPoint = []
    arrayTSPosition = []
    arrayTSOutput = []
    arrayTS = []

    for register in parserFile:
        arrayPixelInfo = []
        arrayPixelInfo.append(register["position"][0])
        arrayPixelInfo.append(register["position"][1])
        arrayPixelInfo.append(register["positionAccuracy"])
        arrayPixel.append(arrayPixelInfo)

        arrayRawPosition.append(register["position"])
        arrayRawAccuracy.append(register["positionAccuracy"])
        arrayRawColor.append(accuracyColorPoint(
            register["positionAccuracy"]))
        arraySmoothedPosition.append(register["smoothedPosition"])
        arraySmoothedAccuracy.append(
            register["smoothedPositionAccuracy"])
        arraySmoothedColorPoint.append(accuracyColorPoint(
            register["smoothedPositionAccuracy"]))
        arrayTSPosition.append(register["positionTS"])
        arrayTSOutput.append(register["positionOutputTS"])
        arrayTS.append(register["positionOutputTS"] - register["positionTS"])

    allTags = True
    drawFileNameTag = drawFileName + ".png"
    rawLevelAccuracy = calculateLevelAccuracy(arrayRawAccuracy)
    smoothedLevelAccuracy = calculateLevelAccuracy(arraySmoothedAccuracy)
    latency = calculateLatency(arrayTS)
    levelLatency = calculateLevelLatency(arrayTS)

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
    queue.put([arrayRawPosition, arrayRawAccuracy, arrayRawColor,
              rawTotalAccuracy, rawLevelAccuracy, arraySmoothedPosition,
              arraySmoothedAccuracy, smoothedTotalAccuracy,
              smoothedLevelAccuracy, file, numFile, drawFileNameTag,
              allTags, arrayPixel, latency, arrayTS, levelLatency])

    for tag in arrayTag:
        arrayPixel = []
        arrayRawPosition = []
        arrayRawAccuracy = []
        arrayRawColor = []
        arraySmoothedPosition = []
        arraySmoothedAccuracy = []
        arraySmoothedColorPoint = []
        arrayTSOutput = []
        arrayTSPosition = []

        for register in parserFile:
            if register["name"] == tag:
                arrayPixelInfo = []
                arrayPixelInfo.append(register["position"][0])
                arrayPixelInfo.append(register["position"][1])
                arrayPixelInfo.append(register["positionAccuracy"])

                arrayPixel.append(arrayPixelInfo)
                arrayRawPosition.append(register["position"])
                arrayRawAccuracy.append(register["positionAccuracy"])
                arrayRawColor.append(accuracyColorPoint(
                    register["positionAccuracy"]))
                arraySmoothedPosition.append(register["smoothedPosition"])
                arraySmoothedAccuracy.append(
                    register["smoothedPositionAccuracy"])
                arraySmoothedColorPoint.append(accuracyColorPoint(
                    register["smoothedPositionAccuracy"]))
                arrayTSOutput.append(register["positionOutputTS"])
                arrayTSPosition.append(register["positionTS"])

        allTags = False
        drawFileNameTag = drawFileName + "_" + tag + ".png"
        rawLevelAccuracy = calculateLevelAccuracy(arrayRawAccuracy)
        smoothedLevelAccuracy = calculateLevelAccuracy(arraySmoothedAccuracy)
        latency = calculateLatency(arrayTS)
        levelLatency = calculateLevelLatency(arrayTS)

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

        queue.put([arrayRawPosition, arrayRawAccuracy, arrayRawColor,
                  rawTotalAccuracy, rawLevelAccuracy, arraySmoothedPosition,
                  arraySmoothedAccuracy, smoothedTotalAccuracy,
                  smoothedLevelAccuracy, file, numFile, drawFileNameTag,
                  allTags, arrayPixel, latency, arrayTS, levelLatency])


# Function to paint the results in a matplot
def paintResult(queue, numRow, outputFolder):
    for result in queue:
        printAccuracyRaw(result[0], result[2], result[3], result[4], result[9],
                         result[10], outputFolder, result[11], result[12],
                         result[14])

        printAccuracyPixel(grid_maker(data=result[13]), result[3],
                           outputFolder, result[11], result[12], result[14])

        printLatencyRaw(result[0], result[15], result[9], result[11],
                        result[12], result[14], result[16])

        printLatencyHistogram(result[15], result[9], result[11], result[12],
                              result[14])


# Function to print the results in a graph
def printAccuracyRaw(arrayPosition, arrayColor, totalAccuracy, levelAccuracy,
                     file, numFile, outputFolder, drawFileName, allTags,
                     latency):
    t = timeit.default_timer()
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
    colors = [ACCURACY_COLOR_LEVEL1, ACCURACY_COLOR_LEVEL2,
              ACCURACY_COLOR_LEVEL3, ACCURACY_COLOR_LEVEL4,
              ACCURACY_COLOR_LEVEL5]
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

    poly_l = get_areas()
    for i in range(len(poly_l)):
        plt.plot(*poly_l[i][1].exterior.xy, 'k')

    plt.savefig((drawFolder + drawFileName), dpi=200)
    plt.clf()
    print("[LOG] [printAccuracyRaw]" + drawFileName + " Raw Created / Time: "
          + str(round((timeit.default_timer()-t), 2)))


# Function to print the results with pixels in a graph
def printAccuracyPixel(array, totalAccuracy, outputFolder, drawFileName,
                       allTags, latency):
    t = timeit.default_timer()
    x = 0
    y = 0
    lenArray = len(array)
    for yPosition in array:
        for xPosition in yPosition:
            plt.plot(x, (lenArray - y), color=accuracyColorPoint(array[y][x]),
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
    print("[LOG] [printAccuracyPixel]" + drawFileName
          + " Pixel Created / Time: "
          + str(round((timeit.default_timer()-t), 2)))


# Function to print the results of the latency in a graph
def printLatencyRaw(arrayPosition, arrayTS, file, drawFileName, allTags,
                    latency, levelLatency):
    t = timeit.default_timer()
    i = 0
    for position in arrayPosition:
        plt.plot(position[0], position[1],
                 color=latencyColorPoint(arrayTS[i]), marker=MARKER)
        i += 1

    plt.xlim(PLOT_X)
    plt.ylim(PLOT_Y)
    plt.axis('off')
    plt.title(drawFileName.replace(".png", "") + "\nMedium Latency: "
              + str(round(latency[0], 2)) + "\nMaximum Latency: "
              + str(latency[1]) + "\nMinimum Latency: " + str(latency[2]))

    texts = ["Level 1", "Level 2", "Level 3", "Level 4", "Level 5"]
    colors = [LATENCY_COLOR_LEVEL1, LATENCY_COLOR_LEVEL2,
              LATENCY_COLOR_LEVEL3, LATENCY_COLOR_LEVEL4,
              LATENCY_COLOR_LEVEL5]
    legendPatches = [plt.plot([], [], marker="o", ms=5, ls="", mec=None,
                     color=colors[i])[0]
                     for i in range(len(texts))]
    plt.legend(legendPatches, levelLatency, loc="lower right",
               frameon=False, fontsize=FONT_SIZE)

    poly_l = get_areas()
    for i in range(len(poly_l)):
        plt.plot(*poly_l[i][1].exterior.xy, 'k')

    varsDrawFolder = drawFileName.split("_")
    if allTags:
        drawFolder = OUTPUT_FOLDER
    else:
        drawFolder = (OUTPUT_FOLDER + varsDrawFolder[0] + "_"
                      + varsDrawFolder[1] + "_" + varsDrawFolder[2] + "/")

    plt.savefig((drawFolder + "Latency_" + drawFileName), dpi=200)
    plt.clf()
    print("[LOG] [printLatencyRaw]" + drawFileName
          + " Latency Created / Time: "
          + str(round((timeit.default_timer()-t), 2)))


# Function to print the results of the latency histogram in a graph
def printLatencyHistogram(arrayTS, file, drawFileName, allTags, latency):
    t = timeit.default_timer()
    plt.hist(arrayTS, color='blue', edgecolor='black', bins=int(180/5))

    plt.title(drawFileName.replace(".png", "") + "\nMedium Latency: "
              + str(round(latency[0], 2)) + "\nMaximum Latency: "
              + str(latency[1]) + "\nMinimum Latency: " + str(latency[2]))

    varsDrawFolder = drawFileName.split("_")
    if allTags:
        drawFolder = OUTPUT_FOLDER
    else:
        drawFolder = (OUTPUT_FOLDER + varsDrawFolder[0] + "_"
                      + varsDrawFolder[1] + "_" + varsDrawFolder[2] + "/")

    plt.savefig((drawFolder + "Histogram_" + drawFileName), dpi=200)
    plt.clf()
    print("[LOG] [printLatencyHistogram]" + drawFileName
          + " Histogram Created / Time: "
          + str(round((timeit.default_timer()-t), 2)))


# Function to create the point with the correct colour
def accuracyColorPoint(value):
    if value == 0:
        return("w")
    if value <= ACCURACY_THRESHOLD_LEVEL1:
        return(ACCURACY_COLOR_LEVEL1)
    elif value <= ACCURACY_THRESHOLD_LEVEL2:
        return(ACCURACY_COLOR_LEVEL2)
    elif value <= ACCURACY_THRESHOLD_LEVEL3:
        return(ACCURACY_COLOR_LEVEL3)
    elif value <= ACCURACY_THRESHOLD_LEVEL4:
        return(ACCURACY_COLOR_LEVEL4)
    else:
        return(ACCURACY_COLOR_LEVEL5)


# Function to create the point with the correct colour
def latencyColorPoint(value):
    if value == 0:
        return("w")
    if value <= LATENCY_THRESHOLD_LEVEL1:
        return(LATENCY_COLOR_LEVEL1)
    elif value <= LATENCY_THRESHOLD_LEVEL2:
        return(LATENCY_COLOR_LEVEL2)
    elif value <= LATENCY_THRESHOLD_LEVEL3:
        return(LATENCY_COLOR_LEVEL3)
    elif value <= LATENCY_THRESHOLD_LEVEL4:
        return(LATENCY_COLOR_LEVEL4)
    else:
        return(LATENCY_COLOR_LEVEL5)


# Function to calculate statistics
def calculateLevelAccuracy(arrayRawAccuracy):
    numLevel1 = 0
    numLevel2 = 0
    numLevel3 = 0
    numLevel4 = 0
    numLevel5 = 0

    for accuracy in arrayRawAccuracy:
        if accuracy <= ACCURACY_THRESHOLD_LEVEL1:
            numLevel1 += 1
        elif accuracy <= ACCURACY_THRESHOLD_LEVEL2:
            numLevel2 += 1
        elif accuracy <= ACCURACY_THRESHOLD_LEVEL3:
            numLevel3 += 1
        elif accuracy <= ACCURACY_THRESHOLD_LEVEL4:
            numLevel4 += 1
        else:
            numLevel5 += 1

    if len(arrayRawAccuracy) == 0:
        numLevel1Percent = 0
    else:
        numLevel1Percent = ("[0-" + str(ACCURACY_THRESHOLD_LEVEL1) + "]: "
                            + str(round(numLevel1 / len(arrayRawAccuracy)
                                  * 100, 2)) + "%")

    if len(arrayRawAccuracy) == 0:
        numLevel2Percent = 0
    else:
        numLevel2Percent = ("[" + str(ACCURACY_THRESHOLD_LEVEL1) + "-"
                            + str(ACCURACY_THRESHOLD_LEVEL2) + "]: "
                            + str(round(numLevel2 / len(arrayRawAccuracy)
                                  * 100, 2)) + "%")

    if len(arrayRawAccuracy) == 0:
        numLevel3Percent = 0
    else:
        numLevel3Percent = ("[" + str(ACCURACY_THRESHOLD_LEVEL2) + "-"
                            + str(ACCURACY_THRESHOLD_LEVEL3) + "]: "
                            + str(round(numLevel3 / len(arrayRawAccuracy)
                                  * 100, 2)) + "%")

    if len(arrayRawAccuracy) == 0:
        numLevel4Percent = 0
    else:
        numLevel4Percent = ("[" + str(ACCURACY_THRESHOLD_LEVEL3) + "-"
                            + str(ACCURACY_THRESHOLD_LEVEL4) + "]: "
                            + str(round(numLevel4 / len(arrayRawAccuracy)
                                  * 100, 2)) + "%")

    if len(arrayRawAccuracy) == 0:
        numLevel5Percent = 0
    else:
        numLevel5Percent = (">" + str(ACCURACY_THRESHOLD_LEVEL4) + ": "
                            + str(round(numLevel5 / len(arrayRawAccuracy)
                                  * 100, 2)) + "%")

    return [numLevel1Percent, numLevel2Percent, numLevel3Percent,
            numLevel4Percent, numLevel5Percent]


# Function to calculate statistics
def calculateLevelLatency(arrayTS):
    numLevel1 = 0
    numLevel2 = 0
    numLevel3 = 0
    numLevel4 = 0
    numLevel5 = 0

    for latency in arrayTS:
        if latency <= LATENCY_THRESHOLD_LEVEL1:
            numLevel1 += 1
        elif latency <= LATENCY_THRESHOLD_LEVEL2:
            numLevel2 += 1
        elif latency <= LATENCY_THRESHOLD_LEVEL3:
            numLevel3 += 1
        elif latency <= LATENCY_THRESHOLD_LEVEL4:
            numLevel4 += 1
        else:
            numLevel5 += 1

    if len(arrayTS) == 0:
        numLevel1Percent = 0
    else:
        numLevel1Percent = ("[0-" + str(LATENCY_THRESHOLD_LEVEL1) + "]: "
                            + str(round(numLevel1 / len(arrayTS)
                                  * 100, 2)) + "%")

    if len(arrayTS) == 0:
        numLevel2Percent = 0
    else:
        numLevel2Percent = ("[" + str(LATENCY_THRESHOLD_LEVEL1) + "-"
                            + str(LATENCY_THRESHOLD_LEVEL2) + "]: "
                            + str(round(numLevel2 / len(arrayTS)
                                  * 100, 2)) + "%")

    if len(arrayTS) == 0:
        numLevel3Percent = 0
    else:
        numLevel3Percent = ("[" + str(LATENCY_THRESHOLD_LEVEL2) + "-"
                            + str(LATENCY_THRESHOLD_LEVEL3) + "]: "
                            + str(round(numLevel3 / len(arrayTS)
                                  * 100, 2)) + "%")

    if len(arrayTS) == 0:
        numLevel4Percent = 0
    else:
        numLevel4Percent = ("[" + str(LATENCY_THRESHOLD_LEVEL3) + "-"
                            + str(LATENCY_THRESHOLD_LEVEL4) + "]: "
                            + str(round(numLevel4 / len(arrayTS)
                                  * 100, 2)) + "%")

    if len(arrayTS) == 0:
        numLevel5Percent = 0
    else:
        numLevel5Percent = (">" + str(LATENCY_THRESHOLD_LEVEL4) + ": "
                            + str(round(numLevel5 / len(arrayTS)
                                  * 100, 2)) + "%")

    return [numLevel1Percent, numLevel2Percent, numLevel3Percent,
            numLevel4Percent, numLevel5Percent]


# Function to calculate the latency
def calculateLatency(arrayTS):
    return (sum(arrayTS) / float(len(arrayTS)), max(arrayTS),
            min(arrayTS))


# Function to create the grid
def grid_maker(size: int = 40, mapa: list = [[-169, 89], [-60, 120]],
               data: list = []):
    a = abs(mapa[0][0] - mapa[0][1])
    b = abs(mapa[1][0] - mapa[1][1])
    pixel_size = min(a, b) / size
    sec_pixel_num = int(max(a, b) / pixel_size)
    array = np.zeros([sec_pixel_num, size])
    super_list = [[0] for x in range(size * sec_pixel_num + 1)]

    for i in data:
        norm = [i[0] - mapa[0][0], i[1] - mapa[1][0]]
        pixel_coord = [int(round(norm[0] / pixel_size)),
                       int(round(norm[1] / pixel_size))]
        pos_s_l = pixel_coord[0] + pixel_coord[1]*sec_pixel_num
        super_list[pos_s_l].append(i[2])

    count = 1
    for i in range(array.shape[1]):
        for j in range(array.shape[0]):
            array[j][i] = np.mean(super_list[count])
            count += 1

    return np.transpose(array)[::-1]


# Function to create the grid
def get_areas():
    file_config = read_json(file_name="/configuration.txt")
    file_areas = areas_ENCE(file_config)
    poly_l = [[key, value['Geometry']] for key, value in file_areas.items()]
    return poly_l
