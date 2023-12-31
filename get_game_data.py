# https://www.youtube.com/watch?v=dQlw1Cdd3pw&list=WL&index=2&t=185s

import os
import json
import shutil # Utility functions for copying and archiving files and directory trees.
from subprocess import PIPE, run
import sys

GAME_DIR_PATTERN = "game"
GAME_CODE_EXTENSION = ".go"
GAME_COMPILE_COMMAND = ["go", "build"]

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

def copy_and_overwrite(source,dest):
    # If dest exists, remove it
    if os.path.exists(dest):
        shutil.rmtree(dest) # recursive delete

    shutil.copytree(source,dest)

def make_json_metadata_file(path, game_dirs):
    data = {
        "gameNames" : game_dirs,
        "numberOfGames" : len(game_dirs)
    }
    with open(path,"w") as f:
        json.dump(data, f)

def compile_game_code(path):
    code_file_name = None
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(GAME_CODE_EXTENSION):
                code_file_name = file
                break
        break
    
    if code_file_name is None:
        return
    
    command = GAME_COMPILE_COMMAND + [code_file_name]
    run_command(command,path)

def run_command(command, path):
    cwd = os.getcwd()
    # change directory
    os.chdir(path)

    # run command in path
    result = run(command, stdout=PIPE, stdin=PIPE, universal_newlines=True)
    print("compile result", result)

    os.chdir(cwd)

def main(source, target):
    cwd = os.getcwd()   # Current Working Directory
    source_path = os.path.join(cwd,source)  # Don't do normal string concat as OS may differ
    target_path = os.path.join(cwd,target) 

    game_paths = find_all_game_paths(source_path)
    # print(game_paths)
    new_game_dirs = get_name_from_paths(game_paths, "game")
    
    create_dir(target_path)

    for src, dest in zip(game_paths, new_game_dirs):
        dest_path = os.path.join(target_path, dest)
        copy_and_overwrite(src, dest_path)
        # compile_game_code(dest_path)

    json_path = os.path.join(target_path, "metadata.json")
    make_json_metadata_file(json_path,new_game_dirs)


if __name__ == "__main__": 
    args = sys.argv # Get command line arguments
    # print(args)

    if len(args) != 3:
        raise Exception("You must a source and target directory only.")
    
    source, target = args[1:]   # First argument is file name
    main(source, target)