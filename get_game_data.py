# https://www.youtube.com/watch?v=dQlw1Cdd3pw&list=WL&index=2&t=185s

import os
import json
import shutil # Utility functions for copying and archiving files and directory trees.
from subprocess import PIPE, run
import sys

GAME_DIR_PATTERN = "game"

def find_all_game_paths(source):
    game_paths = []

    for root, dirs, files in os.walk(source):
        for directory in dirs:
            if GAME_DIR_PATTERN in directory.lower():
                path = os.path.join(source, directory)
                game_paths.append(path)
        break

    return game_paths

def main(source, target):
    cwd = os.getcwd()   # Current Working Directory
    source_path = os.path.join(cwd,source)  # Don't do normal string concat as OS may differ
    target_path = os.path.join(cwd,target) 



if __name__ == "__main__": 
    args = sys.argv # Get command line arguments
    # print(args)

    if len(args) != 3:
        raise Exception("You must a source and target directory only.")
    
    source, target = args[1:]   # First argument is file name
    main(source, target)