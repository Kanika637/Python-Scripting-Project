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
GAME_EXTENSION=".go"
GAME_COMPILE_COMMAND=["go","build"]


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
 
 
 
# for compiling the game code

def compile_game_code(path):
    code_file_name=None
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(GAME_EXTENSION):
                code_file_name=file
                break
            
        break
    
    if code_file_name is None:
        return
    
    command = GAME_COMPILE_COMMAND + [code_file_name]
    run_command(command ,path)
    
def run_command(command, path):
    cwd=os.getcwd()
    #change to the directory where games are
    os.chdir(path)
    
    result =run(command, stdout=PIPE, stdin=PIPE, universal_newlines=True)
    print("Compiled Result is" + result)
    
    #coming back to the directory
    os.chdir(cwd) 
    
    
# removing the "game" name from the paths
def take_certain_path_name(paths, to_strip):
    new_names=[]
    for path in paths:
        # splitting the whole path
        _, dir_name= os.path.split(path)
        # replace the "to_strip" word with empty
        new_dir_name = dir_name.replace(to_strip, "")
        # appending
        new_names.append(new_dir_name)
        
    return new_names 
        
    
   
# copying the games to new directory

def copy_and_overwrite(source, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(source,dest)
    
    
# making some json metadat for our games
def make_json_metadata_file(path, game_dirs):
    data={
        "gameName":game_dirs,
        "numberOfGames":len(game_dirs)
    }
    
    with open(path,"w") as f:
        json.dump(data, f)
           
    
# creating destination directory
def create_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)
        
        
def main(source, target):
    #getting the current working directory
    cwd=os.getcwd()
    #defining source path
    source_path=os.path.join(cwd, source)
    target_path=os.path.join(cwd, target)
    
    game_paths=find_game_paths(source_path)
    #this will give all the game dirs with "game" removed from them
    new_game_dir=take_certain_path_name(game_paths, "_game")
    # print(new_game_dir)
    create_dir(target_path)
    
# zipping means joining both the paths
    for src, dest in zip(game_paths, new_game_dir):
        dest_path=  os.path.join(target_path,dest)
        copy_and_overwrite(src, dest_path)
        compile_game_code(dest_path) 
    
    
    json_path=os.path.join(target_path, "metadata.json")
    make_json_metadata_file(json_path,new_game_dir)
 
if __name__ == "__main__":
    args=sys.argv 
    # they are name of the file, source directory and target directory
    print(args)
    if len(args)!=3:
        raise Exception("You must pass a source and target directory only")
     
    source, target = args[1:]
    main(source,target)