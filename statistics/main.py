# coding=utf-8
# $language = "python"
# $interface = "1.0"

# Main function of the script

# ################### IMPORT ####################
import os

from modules._constants import INPUT_FOLDER, TEMP_FOLDER, OUTPUT_FOLDER
from modules.createJSON import createJSON
from modules.functions import processFile
from modules.structure import initiateStructure, finishStructure


# ################### FUNCTIONS ####################
# Main Function
def main():

    print("\n#################### START ####################")
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    initiateStructure()

    createJSON(INPUT_FOLDER, TEMP_FOLDER, OUTPUT_FOLDER)

    processFile(TEMP_FOLDER, OUTPUT_FOLDER)

    finishStructure()

    print("\n#################### GAME OVER ####################\n")


# ################### EJECUCIÓN ####################
# Ejecución Script
main()
