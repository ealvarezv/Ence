# $language = "python"
# $interface = "1.0"

# Main function of the script

# ################### IMPORT ####################
from modules._constants import INPUT_FOLDER, TEMP_FOLDER, OUTPUT_FOLDER

from modules.functions import createStructure, modifyFile, processFile,\
                              deleteStructure


# ################### FUNCTIONS ####################
# Main Function
def main():

    print("\n#################### START ####################")

    createStructure(TEMP_FOLDER, OUTPUT_FOLDER)

    modifyFile(INPUT_FOLDER, TEMP_FOLDER)

    processFile(TEMP_FOLDER, OUTPUT_FOLDER)

    deleteStructure(TEMP_FOLDER, OUTPUT_FOLDER)

    print("\n#################### GAME OVER ####################\n")


# ################### EJECUCIÓN ####################
# Ejecución Script
main()
