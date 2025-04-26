import subprocess
import os

SOURCE_FILES_TXT_PATH = "config/SOURCE_FILES_LIST.txt"
DELETED_LINES_TXT_PATH = "config/deleted_lines.txt"

if os.path.exists(DELETED_LINES_TXT_PATH):
    os.remove(DELETED_LINES_TXT_PATH)

with open(SOURCE_FILES_TXT_PATH, "r") as file:
    for line in file:
        file_path = line.strip()
        
        # add file name
        c = "echo " + file_path + " >> " + DELETED_LINES_TXT_PATH
        subprocess.run([c], shell=True, text=True)
        # append deleted lines
        c2 = "grep -n -Fxvf regression/*/" + file_path + " orig/" + file_path + " >> " + DELETED_LINES_TXT_PATH
        subprocess.run([c2], shell=True, text=True)
        
