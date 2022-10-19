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
            break
    return res.lower() == 'y'

def files_from_ignore_pattern(files, ignore_double_underscore,ignore_single_underscore):
    print("Following files will be ignored :")
    for file in files:
        if not ((file.startswith("__") and ignore_double_underscore) or (file.startswith("_") and ignore_single_underscore)):
            print(file)

# returns files not to encrypt
def set_files_to_ignore(files):
    print("\n Do you want some files to NOT encrypt? (these files will remain unchanged) (Y/N)")
    if boolean_input():
        print("\nDo you want to ignore all file starting with '__'(double underscore) like __init__.py, __manifest__.py etc ? (Y/N)")
        ignore_double_underscore = boolean_input()
        print("\nDo you want to ignore all file starting with '_'(single underscore) like _custom.py etc ? (Y/N)")
        ignore_single_underscore = boolean_input()
        # TODO ignore file with specified names
        files_from_ignore_pattern(files,ignore_double_underscore,ignore_single_underscore)

def write_config(file, configuration):
    with open(file,"w") as file:
        yaml.dump(configuration,file)

if __name__ == "__main__":
    if verify_arguments():
        original_path = sys.argv[1]
        if os.path.isfile(original_path) and not original_path.endswith(".py"):
            print("ERROR : Not a python file!")
            exit()
        else:
            config = {"path":original_path,
                      "makeNonModular":False,
                      "ignoreFolders":[],
                      "pythonVersion": 3.8}
            if os.path.isfile(original_path):
                #set config
                print("\nConfiguration Done.")
                exit()
            py_files = get_py_files(original_path)
            if len(py_files):
                print("\nTotal {} python file(s) found. Do you want to list? (Y/N)")
                if boolean_input:
                    for file in py_files:
                        print(file)
                set_files_to_ignore(py_files)
            else:
                print("Specified path does not contain any python file. Aborting!")
    else:
        print("ERROR : Please specify a valid path argument!")
        print("e.g. : \n1. python3 autoconfig.py /home/chandsharma/projects/myproject/ (if whole folder/module")
        print("2. python3 autoconfig.py /home/chandsharma/projects/myproject/main.py (if single python file")