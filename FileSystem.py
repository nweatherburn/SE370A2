"""
Nicholas Weatherburn
nwea171 - 2692661
nweatherburn@gmail.com

SoftEng 370 - Assignment 2
"""

import Constants
from FileTrie import FileTrie
import os
import subprocess
import sys


class FileSystem(object):
    def __init__(self):
        self.redirected = not os.isatty(sys.stdin.fileno())
        self.root = FileTrie("", True, None)
        self.current_directory = self.root

        if not os.path.isdir(Constants.DIRECTORY_NAME):
            os.makedirs(Constants.DIRECTORY_NAME)
        else:
            self._build_trie()

    def _build_trie(self):
        for f in os.listdir(Constants.DIRECTORY_NAME):
            self.root.add_file(f[1:], False)

    def execute(self):
        '''Starts this file system operating'''
        line = self._prompt()
        while line != Constants.QUIT:
            command = line.split()[0]
            line = line[len(command):].lstrip()  # Command is the first option

            if command == Constants.PWD:
                self._pwd()

            elif command == Constants.CD:
                self._cd(line)

            elif command == Constants.LS:
                self._ls(line)

            elif command == Constants.RLS:
                self._rls()

            elif command == Constants.TREE:
                self._tree(line)

            elif command == Constants.CLEAR:
                self._clear()

            elif command == Constants.CREATE:
                self._create(line)

            elif command == Constants.ADD:
                self._add(line)

            elif command == Constants.CAT:
                self._cat(line)

            elif command == Constants.DELETE:
                self._delete(line)

            elif command == Constants.DELETE_DIR:
                self._delete_directory(line)

            line = self._prompt()

    def _prompt(self):
        '''Prompts the user for input and returns the user input'''
        if self.redirected:
            user_input = input()
            print(Constants.PROMPT, user_input)
        else:
            print(Constants.PROMPT, end=" ")
            user_input = input()
        return user_input

    def _pwd(self):
        print(self.current_directory.get_full_name())

    def _cd(self, line):
        if len(line) == 0:
            self.current_directory = self.root
        elif line == Constants.PARENT_DIR:
            self.current_directory = self.current_directory.get_parent()
        elif line[0] == Constants.ROOT:
            self.current_directory = self.root.get_directory(line[1:])
        else:
            self.current_directory = self.current_directory.get_directory(line)

    def _ls(self, line):
        if len(line) == 0:
            self.current_directory.list_files()
        elif line[0] == Constants.ROOT:
            directory = self.root.get_directory(line[1:])
            directory.list_files()
        else:
            directory = self.current_directory.get_directory(line)
            directory.list_files()

    def _rls(self):
        subprocess.call(["ls", "-l", Constants.DIRECTORY_NAME])

    def _tree(self, line):
        if len(line) == 0:
            self.current_directory.tree()
        elif line[0] == Constants.ROOT:
            directory = self.root.get_directory(line[1:])
            directory.tree()
        else:
            directory = self.current_directory.get_directory(line)
            directory.tree()

    def _clear(self):
        self.root.delete()

    def _create(self, line):
        if line[0] == Constants.ROOT:
            self.root.add_file(line[1:])
        else:
            self.current_directory.add_file(line)

    def _add(self, line):
        if line[0] == Constants.ROOT:
            index_of_space = line.find(' ')
            f = self.root.get_file(line[1:index_of_space])
            f.append(line[index_of_space + 1:])
        else:
            index_of_space = line.find(' ')
            f = self.root.get_file(line[:index_of_space])
            f.append(line[index_of_space + 1:])

    def _cat(self, line):
        if line[0] == Constants.ROOT:
            f = self.root.get_file(line[1:])
            f.cat()
        else:
            f = self.current_directory.get_file(line)
            f.cat()

    def _delete(self, line):
        if line[0] == Constants.ROOT:
            f = self.root.get_file(line[1:])
            f.delete()
        else:
            f = self.current_directory.get_file(line)
            f.delete()

    def _delete_directory(self, line):
        if line[0] == Constants.ROOT:
            directory = self.root.get_directory(line[1:])
            directory.delete()
        else:
            directory = self.current_directory.get_directory(line)
            directory.delete()


if __name__ == "__main__":
    # Start file system program
    file_system = FileSystem()
    file_system.execute()
