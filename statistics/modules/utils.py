# $language = "python"
# $interface = "1.0"

# Module utils.py

# ################### IMPORT ####################

import collections
import csv
import json
import math
import matplotlib.pyplot as plt
import os
import shapely.geometry

from functools import reduce
from pyproj import Proj, transform


# ################### FUNCTIONS ####################
def quuppaToInter(coord, file_config):
    wgs84 = Proj(init='epsg:4326')  # Degrees 4 digits
    etrs89 = Proj(init='epsg:25829')  # Meters 5 digits

    xpos, ypos = etrs69ToQuuppa(coord, file_config, inverse=True)

    # From etrs89 to International in Lon/Lat
    lonpos, latpos = transform(etrs89, wgs84, xpos, ypos)
    return [lonpos, latpos]


def etrs69ToQuuppa(coord, file_config, inverse=False):
    # Ref in meters of etrs89 (Quuppa center) # SIMPLE TRANSLATION #
    xref = d_get(file_config, 'coordinates.reference_pos')[0]
    yref = d_get(file_config, 'coordinates.reference_pos')[1]
    rot_angle = d_get(file_config, 'coordinates.rot_angle')

    if not inverse:
        # Translation
        xmov = coord[0] - xref
        ymov = coord[1] - yref
        # Rotation
        coordkuppa_x = xmov*math.cos(rot_angle) + ymov * math.sin(rot_angle)
        coordkuppa_y = - xmov*math.sin(rot_angle) + ymov * math.cos(rot_angle)
        return (coordkuppa_x, coordkuppa_y)
    else:
        # Rotation
        xmov = coord[0]*math.cos(rot_angle) + coord[1] * math.sin(rot_angle)
        ymov = - coord[0]*math.sin(rot_angle) + coord[1] * math.cos(rot_angle)
        # Translation
        coordetrs89_x = xref + xmov
        coordetrs89_y = yref + ymov
        return(coordetrs89_x, coordetrs89_y)


def dict_constructor(raw_list, file_config):
    '''
    Dictionary constructor from the csv output

    Parameters
    ----------
    raw_list : list of lists
        DESCRIPTION.

    Returns
    -------
    areas : dictionary
        DESCRIPTION.
    '''
    info = [[item, count] for item, count in collections.Counter(
        [row[2] for row in raw_list]).items() if count > 1]
    aux_list = [1]
    cumul = 1

    for i in range(len(info)):
        cumul += info[i][1]
        aux_list.append(cumul)

    list_polygons = []
    for i in range(len(info)):
        # Coordinates with translation to Quuppa center
        l = [etrs69ToQuuppa([float(raw_list[j][0]), float(raw_list[j][1])],
                               file_config) for j in list(
                                    range(aux_list[i], aux_list[i+1]))]
        list_polygons.append(l)

    areas = {raw_list[i][2]: {'Geometry': shapely.geometry.Polygon(j),
                              'Number_vertices': info[k][1],
                              'Coordinates': j,
                              'Type': raw_list[i][3]} for i, j, k in zip(
                              aux_list[:-1], list_polygons, range(len(info)))}
    return areas


def areas_ENCE(file_config, filepath='data'):
    '''
    ENCE Areas reader from a given csv
    name of the file: Zonas_Ence_25829_m.csv

    Returns
    -------
    dict : Dictionary with id = Area_name.
    '''
    script_dir = os.path.dirname(__file__)
    file_path = filepath + "/" + d_get(file_config, 'coordinates.areas')
    abs_file_path = os.path.join(script_dir, file_path)

    with open(abs_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')  # encoding='utf-8')
        raw_list = list(csv_reader)
    f = dict_constructor(raw_list, file_config)
    return f


def plot_areas(file):
    # Reading from dictionary
    poly_l = [[key, value['Geometry']] for key, value in file.items()]
    fig, ax = plt.subplots()
    for i in range(len(poly_l)):
        ax.plot(*poly_l[i][1].exterior.xy, 'k')  # label=poly_l[i][0])

    # ax.legend(bbox_to_anchor=(1.1, 1.05))
    ax.grid()
    ax.axis('equal')
    plt.subplots_adjust(right=0.6)
    plt.show()


def read_json(file_name, filepath='data'):
    script_dir = os.path.dirname(__file__)
    file_path = filepath + file_name
    abs_file_path = os.path.join(script_dir, file_path)

    with open(abs_file_path, 'r') as txt_file:
        file = json.load(txt_file)
    return file


def d_get(dictionary, keys, default=None):
    return reduce(lambda d, key: d.get(key, default)
                  if isinstance(d, dict)
                  else default, keys.split("."), dictionary)


if __name__ == '__main__':
    file_config = read_json(file_name="/configuration.txt")
    file_areas = areas_ENCE(file_config)
    print(file_areas)
    plot_areas(file_areas)
