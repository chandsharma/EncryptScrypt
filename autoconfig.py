from genericpath import isfile
from platform import python_branch
import sys
import os
from urllib import response
import yaml

def verify_arguments():
    try:
        return os.path.exists(sys.argv[1])
    except:
        return False

# returns list of all python files in given directory
def get_py_files(original_path):
    py_files = []
    for path, subdirs, files in os.walk(original_path):
        py_files_sub = [os.path.join(path, name) for name in files if name.endswith(".py")]
        py_files += py_files_sub
    return py_files

def boolean_input():
    while True:
        res = input(" > ")
        if res.lower() in ["n","y"]:
            return res.lower() == 'y'

def files_from_ignore_pattern(files, ignore_double_underscore):
    files_to_ignore = []
    if ignore_double_underscore:
        print("Files to be ignored :")
        for file in files:
            if file.split('/')[-1].startswith("__") and ignore_double_underscore:
                files_to_ignore.append(file)
                print(file)
        print("No files will be ignored (Reason: No file(s) satiesfy the condition)") if not len(files_to_ignore) else print()
    else:
        print("No files will be ignored.")
    return files_to_ignore

# returns files not to encrypt
def set_files_to_ignore(files):
    print("\n Do you want some files to NOT encrypt? (these files will remain unchanged) (Y/N)")
    if boolean_input():
        print("\nDo you want to ignore all file starting with '__'(double underscore) like __init__.py, __manifest__.py etc ? (Y/N)")
        ignore_double_underscore = boolean_input()
        # TODO ignore file with specified names
        return files_from_ignore_pattern(files,ignore_double_underscore)
    return []

def write_config(file, configuration):
    with open(file,"w") as file:
        yaml.dump(configuration,file)
    print("CONFIGURATION DONE!")

if __name__ == "__main__":
    if verify_arguments():
        original_path = sys.argv[1]
        if os.path.isfile(original_path) and not original_path.endswith(".py"):
            print("ERROR : Not a python file!")
            exit()
        else:
            config_file = "configuration.yaml"
            config = {"path":original_path,
                      "makeNonModular":False,
                      "ignoreFolders":[],
                      "pythonVersion": 3.8,
                      "ignoreFiles":[]}
            config["path"] = original_path
            if os.path.isfile(original_path):
                write_config(config_file,config)
                exit()
            py_files = get_py_files(original_path)
            if len(py_files):
                print("\nTotal {} python file(s) found. Do you want to list? (Y/N)".format(len(py_files)))
                if boolean_input():
                    for file in py_files:
                        print(file)
                config["ignoreFiles"] = set_files_to_ignore(py_files)
                write_config(config_file,config)
            else:
                print("Specified path does not contain any python file. Aborting!")
    else:
        print("ERROR : Please specify a valid path argument!")
        print("e.g. : \n1. python3 autoconfig.py /home/chandsharma/projects/myproject/ (if whole folder/module)")
        print("2. python3 autoconfig.py /home/chandsharma/projects/myproject/main.py (if single python file)")