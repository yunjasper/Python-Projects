# for manipulating the file system, etc.
import os

# this function is copied from here (with modifications):
# https://www.geeksforgeeks.org/rename-multiple-files-using-python/

def rename(path, dirName, newName, extension):
    """
    Renames all the files in a directory. Inputs to the function are the
    path, the name of the directory, the new name format, and the extension
    of the file.
    """
    i = 0

    for filename in os.listdir(path):
        dst = newName + "-" + str(i) + extension
        src = os.path.join(path, filename)
        dst = os.path.join(path, dst)

        os.rename(src,dst)
        i += 1

def helper():
    """Prints the instructions on how to use the command-line program"""
    print("1 -- enter rename process")
    print("2 -- quit")

def chooseOption():
    """Allows user to choose an option and implements basic input sanitation"""
    choice = -1
    while (True):
        choice = input("Choose an option: ")
        try:
            choice = int(choice)
            if choice == 1 or choice == 2:
                break
            else:
                pass
        except ValueError:
            print("illegal input")
            
    return choice

def chooseParams():
    """Allows user to input the path to the directory containing the files to be
        renamed."""
    print("Please use \\ in the path")
    
    while (True):
        path = input("Enter the path of the directory containing the files: ")
        try:
            os.chdir(path)
            dirName = path[path.rfind('\\')+1:len(path)]
            break
        except OSError:
            print("Illegal path")
    
    newName = input("Enter the format of the new names: ")
    extension = input("Enter the file extension: ")
    if extension[0] != ".":
        extension = "." + extension

    return path, dirName, newName, extension

###############################################################

# basic menu system
while (True):
    helper()
    choice = chooseOption()
    if choice == 1:
        (path, dirName, newName, extension) = chooseParams()
        rename(path, dirName, newName, extension)
        print("\n\n")
    elif choice == 2:
        break
