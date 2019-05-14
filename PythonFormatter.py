#!/usr/bin/python

#########################################################################
# For each python file, replace tabs with 4 spaces, and strip trailing
# whitespace if it exists on a line.  Run with --list-only option
# to list Python files without formatting them.
#########################################################################

import sys
import os
import argparse

#########################################################################
# Find the python files for formatting.
#########################################################################

def findPythonFiles(directory, searchRecursive = False, listOnly = False):

    numFiles = 0
    pyFiles = os.listdir(directory)

    for pyFile in pyFiles:
        pyFileFull = os.path.join(directory, pyFile)

        if ((os.path.isdir(pyFileFull)) and (searchRecursive == True)):
            numFiles += findPythonFiles(pyFileFull, True, listOnly)

        elif (pyFileFull.lower().endswith(".py")):
            numFiles += 1
            print pyFileFull

            if listOnly:
                continue
            formatPythonFile(pyFileFull)

    return numFiles

#########################################################################
# Perform formatting: Remove trailing whitespace, tabs become 4 spaces.
#########################################################################

def formatPythonFile(fileToFormat):

    output = ""

    with open (fileToFormat, "r") as inFile:
        for line in inFile:
            line = line.rstrip()
            line = line.replace("\t", "    ")
            output += line + "\n"

    with open (fileToFormat, "w") as outFile:
        outFile.write(output)

#########################################################################
# Main function.
#########################################################################

def main():

    programDescription = ("Ensure consistent Python source formatting.  "
                          "Replace tabs with 4 spaces, remove trailing whitespace.")
    parser = argparse.ArgumentParser(description=programDescription)
    parser.add_argument("-r", "--recursive", help="Search sub-directories recursively",
                        action="store_true")
    parser.add_argument("-l", "--list-only", help="List files only; don't format them",
                        action="store_true")
    parser.add_argument("searchPath", help="Path to search for python files")
    args = parser.parse_args()

    print "Path to search is {0}".format(args.searchPath)

    if args.recursive:
        print "Searching recursively through sub-directories."

    filesProcessed = 0

    if os.path.exists(args.searchPath):
        filesProcessed = findPythonFiles(args.searchPath, args.recursive, args.list_only)
    else:
        print "Path {0} does not exist or is inacessible.\n".format(args.searchPath)
        exit()

    if args.list_only:
        print "Found {0} python files.".format(filesProcessed)
    else:
        print "Processed {0} python files.".format(filesProcessed)

#########################################################################
# Begin!
#########################################################################

if __name__ == "__main__":
    main()
