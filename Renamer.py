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

def RemoveSpace(string):
    """This function takes an input of a string. It outputs a string without any spaces
        at the beginning or end of the string."""
    if len(string)==0:
        pass                    #if string input is empty, then don't do anything
    elif (string[-1]==' '):     #runs only if the last character in the string is a space
        string = string[:-1]    #removes the space
        string=RemoveSpace(string)     #runs recursively to ensure it runs completely
    elif (string[-1]=='\t'):    #if last character in string is a tab-space
        string = string[:-1]    #remove the tab
        string=RemoveSpace(string)
    elif (string[0]==' '):      #runs only if the first character in the string is a space
        string = string[1:]     #removes the space
        string=RemoveSpace(string)     #recursive to ensure all spaces are removed
    elif (string[0]=='\t'):
        string = string[1:]     #if first character in string is a tab-space
        string=RemoveSpace(string)     #remove tab
    return string               #returns a string without a space at the end

def checkNonEmptyInput(string):
    string = RemoveSpace(string)
    if len(string) == 0:
        return 'empty'
    else:
        return string

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
            print("illegal input\n")
            
    return choice

def chooseParams():
    """Allows user to input the path to the directory containing the files to be
        renamed."""
    print("Please use \\ in the path")
    
    while (True):
        # forces user to rename files that are in some directory on the desktop
        # to prevent accidental renaming of important files in the OS
        while (True):
            path = input("Enter the path of the directory containing the files: ")
            if ("c:\\users\\jo\\desktop") not in path.lower():
                if (os.path.exists(path)):
                    print("For safety reasons, renaming files in this directory is not allowed\n")
                else:
                    print("Non-existent path\n")
            elif ("C:\\Users\\JO\\Desktop").lower() in path.lower():
                break
        try:
            os.chdir(path)
            dirName = path[path.rfind('\\')+1:len(path)]
            break
        except OSError:
            print("Non-existent path\n")

    while (True):
        newName = input("Enter the format of the new names: ")
        stripped = checkNonEmptyInput(newName)
        if stripped != "empty":
            break
    
    while (True):
        extension = input("Enter the file extension: ")
        stripped = checkNonEmptyInput(extension)
        if stripped != "empty":
            break
        
    if extension[0] != ".":
        extension = "." + extension

    return path, dirName, newName, extension

def checkProceed():
    """Basic check for whether user wants to proceed. Returns 1 if the user wants to
        proceed; returns 2 if the user aborts the rename process."""
    print("Are you sure you want to proceed? Enter: \n")
    print("1 -- proceed with renaming")
    print("2 -- abort rename process")
    choice = chooseOption()
    return choice

###############################################################

# basic menu system
while (True):
    helper()
    choice = chooseOption()
    if choice == 1:
        (path, dirName, newName, extension) = chooseParams()
        go = checkProceed()
        if go == 1:
            rename(path, dirName, newName, extension)
            print("\nRename EXECUTED")
        else:
            print("\nRename CANCELLED")
        print("\n")
    elif choice == 2:
        break
