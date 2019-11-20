# for manipulating the file system, etc.
import os

# this function is copied from here (with modifications):
# https://www.geeksforgeeks.org/rename-multiple-files-using-python/

def rename(path, dirName, newName):
    """
    Renames all the files in a directory. Inputs to the function are the
    path, the name of the directory, the new name format, and the extension
    of the file.
    """
    i = 1

    for filename in os.listdir(path):
        ext = filename[filename.rfind('.'): len(filename)]
        dst = newName + "-" + str(i) + ext
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
    print("1 -- begin rename process")
    print("2 -- quit")

def chooseParams(safePath):
    """Allows user to input the path to the directory containing the files to be
        renamed, and choose the format of the new file names."""
    print("Please use \\ in the path")
    
    while (True):
        # forces user to rename files that are in some directory on the desktop
        # to prevent accidental renaming of important files in the OS
        while (True):
            path = input("\nEnter the path of the directory containing the files: ")

            # using lower() makes directory path case insensitive
            if safePath.lower() not in path.lower():
                if (os.path.exists(path)):
                    print("For safety reasons, renaming files in this directory is not allowed\n")
                else:
                    print("Non-existent path\n")
            elif safePath.lower() in path.lower():
                print("The current path is: " + path.lower())
                choice = checkProceed()
                if choice == 1:
                    break
                if choice == 2:
                    pass
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
    return path, dirName, newName


def successRename(path, dirName, newName):
    """checks whether the rename operation was successful by comparing the new names
        of every file with the specified newName format"""
    os.chdir(path)
    renamed = os.listdir(path) # this is a list
    renamed.sort(key = len)
    
    i = 1
    flag = True
    for j in range(len(renamed)):
        nameFormat = newName + "-" + str(i)
        if nameFormat in renamed[j]:
            #print(str(i) + " success")
            pass
        else:
            print(str(i) + " -- " + nameFormat + " failed")
            flag = False
        i += 1
    return flag

def checkProceed():
    """Basic check for whether user wants to proceed. Returns 1 if the user wants to
        proceed; returns 2 if the user aborts the rename process."""
    print("Are you sure you want to proceed? Enter: \n")
    print("1 -- proceed with renaming")
    print("2 -- return to previous step")
    choice = chooseOption()
    return choice

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

###############################################################

# basic menu system
while (True):
    user = input("Enter your username: ")
    if (os.path.exists(os.path.join("C:\\users\\",user))):
        print('')
        break
    else:
        print("User does not exist\n")
safePath = os.path.join("C:\\Users\\", user, "desktop")

while (True):
    helper()
    choice = chooseOption()
    if choice == 1:
        (path, dirName, newName) = chooseParams(safePath)
        print("You are about to rename the files in: \t " + path)
        print("to the format: \t " + newName + "-(index)\n")
        go = checkProceed()
        if go == 1:
            rename(path, dirName, newName)
            print("\nRename EXECUTED")
            print("Checking status...")
            successRename(path, dirName, newName)
        else:
            print("\nRename CANCELLED")
        print("\n")
    elif choice == 2:
        print("Program terminated.")
        break
