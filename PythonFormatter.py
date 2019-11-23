#!/usr/bin/env python
# -*- coding: utf-8 -*-

#################################################################################################
# For each python file in the provided directory, replace tabs with 4 spaces, and strip trailing
# whitespace if it exists on a line.
# Run with --list-only option to list Python files without formatting them.
# Run with --recursive option to recursively search subdirectories.
#################################################################################################

import os
import argparse


class PythonFormatter:

    def __init__(self, search_recursive, list_only):
        self.search_recursive = search_recursive
        self.list_only = list_only
        self.file_count = 0

    def process_python_files(self, directory):
        """ Locate python files, pass each one to the format method.  Return the count of files found

            Arguments:
            directory - the folder in which to search.
        """

        py_files = os.listdir(directory)

        for py_file in py_files:
            py_file_full_path = os.path.join(directory, py_file)

            if os.path.isdir(py_file_full_path) and self.search_recursive:
                self.process_python_files(py_file_full_path)

            elif py_file_full_path.lower().endswith(".py"):
                self.file_count += 1
                print(py_file_full_path)

                if self.list_only:
                    continue
                self.format_python_file(py_file_full_path)

        return self.file_count

    def format_python_file(self, file_to_format):
        """ Strip whitespace, and replace tabs with spaces. Return True if successful, otherwise False.

            Arguments:
            file_to_format - the full path to the file to format.
        """

        output = ""
        is_successful = True

        try:
            with open(file_to_format, "r") as inFile:
                for line in inFile:
                    line = line.rstrip()
                    line = line.replace("\t", "    ")
                    output += line + "\n"

            with open(file_to_format, "w") as outFile:
                outFile.write(output)
        except FileNotFoundError as not_found:
            print(not_found.strerror)
            is_successful = False
        except PermissionError as permissions:
            print(permissions.strerror)
            is_successful = False

        return is_successful

#########################################################################
# Main function.
#########################################################################


def main():

    program_description = ("Ensure consistent Python source formatting.  "
                           "Replace tabs with 4 spaces, remove trailing whitespace.")
    parser = argparse.ArgumentParser(description=program_description)
    parser.add_argument("-r", "--recursive", help="Search sub-directories recursively",
                        action="store_true")
    parser.add_argument("-l", "--list-only", help="List files only; don't format them",
                        action="store_true")
    parser.add_argument("searchPath", help="Path to search for python files")
    args = parser.parse_args()

    print("Path to search is:", args.searchPath)

    if args.recursive:
        print("Searching recursively through subdirectories.")

    files_processed = 0
    formatter = PythonFormatter(args.recursive, args.list_only)

    if os.path.exists(args.searchPath):
        files_processed = formatter.process_python_files(args.searchPath)
    else:
        print("Path", args.searchPath, "does not exist or is inaccessible.\n")
        exit()

    if args.list_only:
        print("Found",  files_processed, "python files.")
    else:
        print("Processed",  files_processed, "python files.")

#########################################################################
# Begin!
#########################################################################


if __name__ == "__main__":
    main()
