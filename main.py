# $language = "python"
# $interface = "1.0"

# Main function of the script

# ################### IMPORT ####################
from modules.functions import createStructure, modifyFile, processFile,\
                              deleteStructure

# ################### VARS ####################
# Ruta de Carpetas
inputFolder = "_input/"
tempFolder = "ztemp/"
outputFolder = "_output/"


# ################### FUNCTIONS ####################
# Main Function
def main():

    print("\n#################### START ####################")

    createStructure(tempFolder, outputFolder)

    modifyFile(inputFolder, tempFolder)

    processFile(tempFolder, outputFolder)

    deleteStructure(tempFolder, outputFolder)

    print("\n#################### GAME OVER ####################\n")


# ################### EJECUCIÓN ####################
# Ejecución Script
main()
