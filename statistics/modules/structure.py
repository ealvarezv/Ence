# $language = "python"
# $interface = "1.0"

# Module structure.py

# ################### IMPORT ####################
import os
import shutil


# ################### CONSTANTS ####################
from modules._constants import TEMP_FOLDER, OUTPUT_FOLDER


# ################### FUNCTIONS ####################
# Function to create the structure for temporal files
def initiateStructure():
    print("\n########## initiateStructure ##########")
    createFolder(TEMP_FOLDER)
    createFolder(OUTPUT_FOLDER)


# Function to create a folder
def createFolder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
        print("[LOG] [createFolder] " + folder + " created")
    else:
        print("[LOG] [createFolder] " + folder + " already exists")


# Function to delete the structure for temporal files
def finishStructure():
    print("\n########## finishStructure ##########")
    createFolder(OUTPUT_FOLDER)
    moveFiles(TEMP_FOLDER, OUTPUT_FOLDER)
    deleteFolder(TEMP_FOLDER)


# Function to move files between two folder
def moveFiles(srcFolder, dstFolder):
    if os.path.exists(srcFolder):
        listFile = os.listdir(srcFolder)
        for file in listFile:
            src = srcFolder + file
            dst = dstFolder + file
            shutil.move(src, dst)
        print("[LOG] [moveFiles] Log Files copied from " + srcFolder
              + " to " + dstFolder)
    else:
        print("[ERROR] [moveFiles] " + srcFolder + " does not exists")


# Function to delete a folder
def deleteFolder(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder, ignore_errors=True)
        print("[LOG] [deleteFolder] " + folder + " deleted")
    else:
        print("[ERROR] [deleteFolder] " + folder + " does not exists")
