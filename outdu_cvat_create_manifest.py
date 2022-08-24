import subprocess
import os
import sys
import datetime

def buildKeyFrameExtractCommand(path, file):

    print(file)
    user_input_dict = {}

    user_input_dict["input_file"] = os.path.join(path,file)
    dir_name = os.path.splitext(file)[0]
    user_input_dict["output_dir"] = os.path.join(path, dir_name)
    user_input_dict["output_files"] = user_input_dict["output_dir"]+"/"+dir_name+"_%4d.jpg"
    
    commands_list1 = [
	"mkdir",
    "-p",
	user_input_dict["output_dir"]
    ]

    commands_list2 = [
        "ffmpeg",
        "-i",
        user_input_dict["input_file"],
        "-vf",
        "select='eq(pict_type,I)'",
        "-vsync",
        "vfr",
        user_input_dict["output_files"]
        ]
        
    commands_list3 = [
	"mv",
	user_input_dict["input_file"],
	user_input_dict["output_dir"]
    ]

    return [commands_list1, commands_list2, commands_list3]

def buildManifestCreateCommand(dirpath, create_manifest):
    commands1 = [
	"python3",
	create_manifest,
	"--output-dir",
	dirpath,
	dirpath
    ]
    
    return [commands1]

def buildProcessedCommand(dirpath, output_dir):
    commands2 = [
    "mv",
    dirpath,
    output_dir
    ]
    
    return [commands2]    

def runCommands(commands_all):

    for commands in commands_all:
        print(commands)
        if subprocess.run(commands).returncode == 0:
            print ("Script Ran Successfully")
        else:
            print ("There was an error running your script")
            break


print(datetime.datetime.now())
path=sys.argv[1]
output_path=sys.argv[2]
create_manifest_script_path=sys.argv[3]

buckets = (file for file in os.listdir(path) 
         if os.path.isdir(os.path.join(path, file)))

for bucket in buckets:
    print(bucket)
    output_bucket_path=os.path.join(output_path, bucket)
    commands_list1 = [
    "mkdir",
    "-p",
    output_bucket_path
    ]
    runCommands([commands_list1])

    bucket_path=os.path.join(path, bucket)

    files = (file for file in os.listdir(bucket_path) 
             if os.path.isfile(os.path.join(bucket_path, file)))
      
    for file in files:   
        print(file)      
        runCommands(buildKeyFrameExtractCommand(bucket_path, file))
        
    dirs = (file for file in os.listdir(bucket_path) 
             if os.path.isdir(os.path.join(bucket_path, file)))
             
    for dir in dirs:
        print(dir)
        dirpath=os.path.join(bucket_path,dir)
        if not os.path.exists(os.path.join(dirpath, "manifest.jsonl")):
            runCommands(buildManifestCreateCommand(dirpath, create_manifest_script_path))
        runCommands(buildProcessedCommand(dirpath, output_bucket_path))        