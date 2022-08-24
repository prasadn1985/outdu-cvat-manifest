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

def buildManifestCreateCommand(dirpath, create_manifest, output_dir):
    commands1 = [
	"python3",
	create_manifest,
	"--output-dir",
	dirpath,
	dirpath
    ]
    
    commands2 = [
    "mv",
    dirpath,
    output_dir
    ]
    return [commands1, commands2]  

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
create_manifest_script_path=sys.argv[2]

buckets = (file for file in os.listdir(path) 
         if os.path.isdir(os.path.join(path, file)))

for bucket in buckets:
    print(bucket)
    output_bucket_path1=os.path.join(path, bucket)
    output_bucket_path=os.path.join(output_bucket_path1, "processed")
    commands_list1 = [
    "mkdir",
    "-p",
    output_bucket_path
    ]
    runCommands([commands_list1])

    bucket_path1=os.path.join(path, bucket)
    bucket_path=os.path.join(bucket_path1, "wip")

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
        runCommands(buildManifestCreateCommand(dirpath, create_manifest_script_path, output_bucket_path))