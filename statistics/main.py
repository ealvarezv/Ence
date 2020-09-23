# $language = "python"
# $interface = "1.0"

# Main function of the script

# ################### IMPORT ####################
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from modules._constants import INPUT_FOLDER, TEMP_FOLDER, OUTPUT_FOLDER

from modules.createJSON import createJSON

from modules.functions import processFile

from modules.structure import initiateStructure, finishStructure


# ################### FUNCTIONS ####################
# Main Function
def main():

    print("\n#################### START ####################")

    initiateStructure()

    createJSON(INPUT_FOLDER, TEMP_FOLDER, OUTPUT_FOLDER)

    processFile(TEMP_FOLDER, OUTPUT_FOLDER)

    finishStructure()

    print("\n#################### GAME OVER ####################\n")


# ################### EJECUCION ####################
# Ejecucion Script
main()
