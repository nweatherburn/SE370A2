"""
Nicholas Weatherburn
nwea171 - 2692661
nweatherburn@gmail.com

SoftEng 370 - Assignment 2
"""

import Constants
from FileTrie import FileTrie
import os
import sys


class FileSystem(object):
    def __init__(self):
        self.file_trie = FileTrie()
        self.redirected = not os.isatty(sys.stdin.fileno())

    def execute(self):
        '''Starts this file system operating'''
        line = self._prompt()
        while line != Constants.QUIT:
            print(line)

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


if __name__ == "__main__":
    file_system = FileSystem()
    file_system.execute()
