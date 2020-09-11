# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 16:51:22 2020

@author: crguerrero
"""

from modules._constants import OUTPUT_FOLDER, MARKER
from modules.utils import read_json, areas_ENCE
import numpy as np
import matplotlib.pyplot as plt


def grid_maker(size: int = 40, mapa: list = [[-169, 89], [-60, 120]],
               data: list = []):
    a = abs(mapa[0][0] - mapa[0][1])
    b = abs(mapa[1][0] - mapa[1][1])

    pixel_size = min(a, b) / size
    sec_pixel_num = int(max(a, b) / pixel_size)

    array = np.zeros([sec_pixel_num, size])

    # List that contains a list of 3 entries [coordX, coordY, accuracy]
    super_list = [[0] for x in range(size * sec_pixel_num + 1)]

    for i in data:
        norm = [i[0] - mapa[0][0], i[1] - mapa[1][0]]
        # print(norm)
        pixel_coord = [int(round(norm[0] / pixel_size)),
                       int(round(norm[1] / pixel_size))]
        # print(pixel_coord)
        # Super list position:

        pos_s_l = pixel_coord[0] + pixel_coord[1]*sec_pixel_num
        # print(pos_s_l)
        super_list[pos_s_l].append(i[2])

    # print(super_list)
    # Fill the array:
    count = 1
    for i in range(array.shape[1]):
        for j in range(array.shape[0]):
            array[j][i] = np.mean(super_list[count])
            count += 1

         # array[pixel_coord[0]-1][pixel_coord[1]-1] = i[2]
    return np.transpose(array)[::-1]


# def get_areas():
#     file_config = read_json(file_name="/configuration.txt")
#     file_areas = areas_ENCE(file_config)
#     poly_l = [[key, value['Geometry']] for key, value in file_areas.items()]
#     return poly_l


def plot_accuracy(array, arrayPosition, arrayColor, totalAccuracy, levelAccuracy, file,
                numFile, outputFolder, drawFileName, allTags):
    # poly_l = get_areas()


    # fig4 = plt.figure(figsize=(12, 9))
    # ax_2 = fig4.add_subplot(111)
    #
    # for i in range(len(poly_l)):
    #     ax_2.plot(*poly_l[i][1].exterior.xy, 'k')#, label=poly_l[i][0])
    # fontP = FontProperties()
    # fontP.set_size('xx-small')
    # ax_2.legend(loc="lower right", prop=fontP)
    # ax_2.set_xlabel('X Label')
    # ax_2.set_ylabel('Y Label')

    # fig3 = plt.figure(figsize=(12, 9))
    # ax_3 = fig3.add_subplot(111)
    # im = ax_3.imshow(array, cmap='hot_r')
    # plt.show()
    x = 0
    y = 0

    for yPosition in array:
        for xPosition in yPosition:
            print(str(x) + "," + str(y))
            plt.plot(x, y, color=colorPoint(array[x][y]), marker="s")
            x += 1
        y += 1
        x = 0
        # plt.plot(position[0], position[1], color=arrayColor[i], marker=MARKER)
        # i += 1

    # plt.xlim(PLOT_X)
    # plt.ylim(PLOT_Y)
    # plt.axis('off')
    # plt.title(drawFileName.replace(".png", "")
    #           + "\nAccuracy : " + str(totalAccuracy))
    #
    # texts = ["Level 1", "Level 2", "Level 3", "Level 4", "Level 5"]
    # colors = [COLOR_LEVEL1, COLOR_LEVEL2, COLOR_LEVEL3, COLOR_LEVEL4,
    #           COLOR_LEVEL5]
    # legendPatches = [plt.plot([], [], marker="o", ms=5, ls="", mec=None,
    #                  color=colors[i])[0]
    #                  for i in range(len(texts))]
    # plt.legend(legendPatches, levelAccuracy, loc="lower right", frameon=False,
    #            fontsize=FONT_SIZE)
    #
    plt.show()
    varsDrawFolder = drawFileName.split("_")
    if allTags:
        drawFolder = OUTPUT_FOLDER
    else:
        drawFolder = (OUTPUT_FOLDER + varsDrawFolder[0] + "_"
                      + varsDrawFolder[1] + "_" + varsDrawFolder[2] + "/")

    plt.savefig((drawFolder + "Pixel" + drawFileName), dpi=200)
    plt.clf()
