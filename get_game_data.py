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
        for directory in dirs:  # dirs has names not full path
            if GAME_DIR_PATTERN in directory.lower():
                path = os.path.join(source, directory)
                game_paths.append(path)
        break   # os.walk runs recursively for inner directories but we only want one level

    return game_paths

def get_name_from_paths(paths, to_strip): # Remove "to_strip" from each path in paths
    new_names = []
    for path in paths:
        # Split - Returns tuple "(head, tail)" where "tail" is everything after the final slash.
        _ , dir_name = os.path.split(path)
        new_dir_name = dir_name.replace(to_strip,"")
        new_names.append(new_dir_name)

    return new_names

def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)

def copy():
    pass


def main(source, target):
    cwd = os.getcwd()   # Current Working Directory
    source_path = os.path.join(cwd,source)  # Don't do normal string concat as OS may differ
    target_path = os.path.join(cwd,target) 

    game_paths = find_all_game_paths(source_path)
    # print(game_paths)
    new_game_dirs = get_name_from_paths(game_paths, "game")

    create_dir(target_path)

if __name__ == "__main__": 
    args = sys.argv # Get command line arguments
    # print(args)

    if len(args) != 3:
        raise Exception("You must a source and target directory only.")
    
    source, target = args[1:]   # First argument is file name
    main(source, target)