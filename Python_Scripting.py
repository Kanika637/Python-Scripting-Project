import os
import json
# for copying and overwriting actions
import shutil
#for terminal arguments so that we can compil and run go commands
from subprocess import PIPE, run
#for accessing the command line arguments
import sys

#will be finding this word in the game directories
GAME_PATTERN= "game"


#getting full path of all the games which have the word "game "in them
def find_game_paths(source):
    game_paths=[]
    
    for root, dirs, files in os.walk(source):
        for directory in dirs:
            if GAME_PATTERN in directory.lower():
                path=os.path.join(source,directory)
                game_paths.append(path)
        break
    return game_paths
 
 
# removing the "game" name from the paths
def take_certain_payh_name(path, to_strip):
    pass
          
    
# creating destination directory
def create_dir(path):
    if not os.path.exists():
        os.mkdir(path)
        
        
def main(source, target):
    #getting the current working directory
    cwd=os.getcwd()
    #defining source path
    source_path=os.path.join(cwd, source)
    target_path=os.path.join(cwd, target)
    
    game_paths=find_game_paths(source_path)
    create_dir(target_path)
    
 
if __name__ == "__main__":
    args=sys.argv
    # they are name of the file, source directory and target directory
    print(args)
    if len(args)!=3:
        raise Exception("You must pass a source and target directory only")
     
    source, target = args[1:]
    main(source,target)