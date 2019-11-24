
"""
This program batch renames files. The user specifies a directory that must
be a subdirectory of the Desktop; this is required so that critical files
are not accidentally renamed.

Once the directory is specified, the user can specify a format for which
all of the files will be renamed to. An index is appended to the end of
the given format, and then the file is renamed. Note that directories
within the specified directory will be ignored.

After the renaming process, a function runs to check that the files were
renamed properly.

The program contains code to allow cancellation of certain steps in the
renaming procedure.

Different versions of this program can be found in the commit history here:
https://github.com/yunjasper/Python-Projects/blob/master/Renamer.py

Author: Jasper Yun
Date:   2019-11-20
"""

import os, ctypes

def RemoveSpace(string):
    """This function takes an input of a string. It outputs a string without any spaces
        at the beginning or end of the string."""
    if len(string)==0:
        pass                    # if string input is empty, then don't do anything
    elif (string[-1]==' '):     # runs only if the last character in the string is a space
        string = string[:-1]    # removes the space
        string=RemoveSpace(string)     # runs recursively to ensure it runs completely
    elif (string[-1]=='\t'):    # if last character in string is a tab-space
        string = string[:-1]    # remove the tab
        string=RemoveSpace(string)
    elif (string[0]==' '):      # runs only if the first character in the string is a space
        string = string[1:]     
        string=RemoveSpace(string)     # recursive to ensure all spaces are removed
    elif (string[0]=='\t'):
        string = string[1:]     # if first character in string is a tab-space
        string=RemoveSpace(string)     # recursive to remove all tabs
    return string               # returns a string without a space at the end

def checkNonEmptyInput(string):
    """Checks that the input is not an empty string or that the input is not
        entirely composed of whitespace (tabs, spaces)"""
    string = RemoveSpace(string)
    if len(string) == 0:
        return 'empty'
    else:
        return string

def checkProceed():
    """Basic check for whether user wants to proceed. Returns 1 if the user wants to
        proceed; returns 2 if the user aborts the rename process."""
    print("Are you sure you want to proceed? Enter: \n")
    print("1 -- proceed with renaming")
    print("2 -- abort current operation")
    choice = chooseOption()                 # input sanitization
    return choice

def chooseOption():
    """Allows user to choose an option and implements basic input sanitization"""
    while (True):
        choice = input("Choose an option: ")
        try:
            choice = int(choice)
            if choice == 1 or choice == 2:
                break
            else:       # pass returns to top of while loop, allowing new option choice
                pass
        except ValueError:
            print("illegal input\n")
            
    return choice

def helper():
    """Prints the instructions on how to use the command-line program"""
    print("RENAMER: easily batch rename files (not folders)")
    print("1 -- begin rename process")
    print("2 -- exit")

def chooseParams(safePath, prohibitedChars):
    """Allows user to input the path to the directory containing the files to be
        renamed, and choose the format of the new file names."""
    print("Please use \\ in the path")
    
    while (True):
        # forces user to rename files that are in some directory on the desktop
        # to prevent accidental renaming of important files in the OS
        print("\nNote that the folder containing the files to be renamed " +
                  "must be a subfolder of the Desktop.")
        print("As such, enter a path beginning from the Desktop.")
        while (True):
            path = input("\nPath to the directory containing the" + 
                         " files to be renamed: ")
            path = os.path.join(safePath, path)
            
            # check to see if the path exists
            if os.path.exists(path) == False:
                print("Non-existent path\n")
            elif safePath.lower() in path.lower(): # lower() makes paths case-insensitive
                print("\nThe current path is: " + path.lower())
                choice = checkProceed()
                if choice == 1:
                    break
                if choice == 2: # pass returns to top of while loop - choose new path
                    pass
        try:
            os.chdir(path)  # change directory to the one specified by the path
            break
        except OSError:     # if path does not exist, catch the error
            print("Non-existent path\n")

    # check if user wants to display the files in the specified directory
    printFilesInDir(path)

    # check if user wants to proceed with this folder
    choice = checkProceed()
    if choice == 1:
        print("ok")
    if choice == 2:
        pass
    
    # input the file names format
    # a check is performed to see if any prohibited characters are in the format name
    choose = False
    while (choose == False):
        newName = input("\nEnter the format of the new names: ")
        stripped = checkNonEmptyInput(newName) # input sanitization
        if stripped != "empty":                # non-empty input, so exit while loop
            passed = 0
            for i in prohibitedChars:
                if i in stripped:
                    choose = False
                    print("Your format contains prohibited characters. Try again.")
                    print("The prohibited characters are: ")
                    listedChars = ''
                    for i in prohibitedChars:
                        listedChars += i + ' '
                    print(listedChars)
                    break
                else:
                    passed += 1
            if passed == len(prohibitedChars):
                break
    return path, newName


def printFilesInDir(path):
    """Prints the files in the current directory specified by the input variable, path"""
    print("\nWould you like to see the files in this folder? Please choose an option:")
    print("1 -- display the files in this folder")
    print("2 -- pass")
    choice = chooseOption()
    if choice == 1:
        files = os.listdir(path)
        if len(files) > 50:
            print("There are more than 50 files in this directory.")
            print("1 -- display all files")
            print("2 -- display the first 50 files")
            choice2 = chooseOption()
            if choice2 == 1:
                for i in files:
                    if (os.path.isfile(os.path.join(path, i))):
                        print("File:\t %s" %(i))
                    elif (os.path.isdir(os.path.join(path, i))):
                        print("Folder:\t %s" %(i))
                    else:
                        print("Object:\t %s" %(i))
            else:
                for i in range(50):
                    if (os.path.isfile(os.path.join(path, files[i]))):
                        print("File:\t %s" %(i))
                    elif (os.path.isdir(os.path.join(path, files[i]))):
                        print("Folder:\t %s" %(i))
                    else:
                        print("Object:\t %s" %(files[i]))
        else:
            for i in files:
                if (os.path.isfile(os.path.join(path, i))):
                    print("File:\t %s" %(i))
                elif (os.path.isdir(os.path.join(path, i))):
                    print("Folder:\t %s" %(i))
                else:
                    print("Object:\t %s" %(i))
    if choice == 2:
        pass


# this function is copied from here (with modifications):
# https://www.geeksforgeeks.org/rename-multiple-files-using-python/

def rename(path, newName):
    """
    Renames all the files in a directory. Inputs to the function are the
    path, the name of the directory, the new name format, and the extension
    of the file.
    """
    i = 1
    # rename each file:
    for filename in os.listdir(path):
        # check that we are renaming FILES only, not folders
        if (os.path.isfile(os.path.join(path, filename))):
            ext = filename[filename.rfind('.'): len(filename)]
            dst = newName + "-" + str(i) + ext
            src = os.path.join(path, filename)
            dst = os.path.join(path, dst)

            os.rename(src,dst)
            i += 1  # incrememnt the index
        else:       # for objects that are not files, we simply pass
            pass

def successRename(path, newName):
    """checks whether the rename operation was successful by comparing the new names
        of every file with the specified newName format"""
    os.chdir(path)
    renamed = os.listdir(path)  # this is a list
    toRem = []                  # empty list of strings to be removed from renamed
    for i in renamed:
        if os.path.isfile(os.path.join(path, i)) == False: # deals with *any* non-files
            toRem.append(i)
    for i in toRem:
        renamed.remove(i)

    renamed.sort(key = len)     # sort list by the index
    i = 1
    flag = True                 # to check if the rename was successful
    for j in range(len(renamed)):
        nameFormat = newName + "-" + str(i)
        if nameFormat in renamed[j]:
            #print(str(i) + " success")
            pass
        else:
            print(str(i) + " -- " + nameFormat + " failed")
            flag = False        # return false if any renamed files do not match
        i += 1
    return flag

###############################################################

prohibitedChars = ['>','<',':','"','/','\\','|','?','*',]

try:
 is_admin = os.getuid() == 0
except AttributeError:
 is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

print(is_admin)

# basic menu system
while (True):
    user = input("Enter your username: ")

    # check if user exists:
    if (os.path.exists(os.path.join("C:\\users\\",user))): 
        print('')
        break
    else:
        print("User does not exist\n")

# we require that the directory containing the files to be renamed
# be a subdirectory of the Desktop; this is for safety reasons
safePath = os.path.join("C:\\Users\\", user, "desktop")

while (True):
    helper()        # print the "menu"
    choice = chooseOption()
    
    if choice == 1: # enter the renaming process
        
        (path, newName) = chooseParams(safePath, prohibitedChars)
        print("You are about to rename the files in: \t " + path)
        print("to the format: \t " + newName + "-(index)\n")

        # let user confirm and proceed to renaming
        go = checkProceed()
        if go == 1:
            rename(path, newName)
            print("\nRename EXECUTED")
            print("Checking status...")
            flag = successRename(path, newName)
            if flag == True:
                print("Successfully renamed all files.")
            else:
                print("Some files were not able to be renamed correctly.")
        else:
            print("\nRename CANCELLED")
        print("\n")
    
    elif choice == 2: # exit the program
        print("\nProgram terminated.")
        break
