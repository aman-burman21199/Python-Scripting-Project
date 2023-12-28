import os
import json
import shutil # Utility functions for copying and archiving files and directory trees.
from subprocess import PIPE, run
import sys

if __name__ == "__main__": 
    args = sys.argv # Get command line arguments
    # print(args)

    if len(args) != 3:
        raise Exception("You must a source and target directory only.")
    
    source, target = args[1:]   # First argument is file name