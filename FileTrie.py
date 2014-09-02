"""
Nicholas Weatherburn
nwea171 - 2692661
nweatherburn@gmail.com

SoftEng 370 - Assignment 2

FileTrie to be used in this assignment.
More information on Tries can be found here:
http://en.wikipedia.org/wiki/Trie
"""

import Constants


class FileTrie(object):
    def __init__(self, name, is_directory, parent):
        self.name = name
        self.directory = is_directory
        self.children = {}
        self.parent = parent

    def is_directory(self):
        return self.directory

    def is_file(self):
        return not self.is_directory

    def get_name(self):
        return self.name

    def get_full_name(self):
        if self.parent:
            full_name = self.parent.get_full_name() + self.get_name()
            if self.is_directory():
                full_name += Constants.DIRECTORY_DIVIDER
            return full_name
        else:
            return Constants.ROOT

    def add_file(self, filename):
        path = filename.split(Constants.DIRECTORY_DIVIDER)
        self._add_file(path)

    def _add_file(self, path):
        if len(path) == 1:
            # Is file
            self.children[path[0]] = FileTrie(path[0], False, self)
            self.children[path[0]]._create_as_file()
        else:
            child = FileTrie(path[0], True, self)
            self.children[path[0]] = child
            child._add_file(path[1:])

    def get_parent(self):
        return self.parent

    def get_directory(self, directory_name):
        path = directory_name.split(Constants.DIRECTORY_DIVIDER)
        return self._get_directory(path)

    def _get_directory(self, path):
        if len(path) == 0:
            # We're in directory
            return self
        else:
            self.children[path[0]]._get_directory(path[1:])

    def _create_as_file(self):
        file_name = Constants.DIRECTORY_NAME + '/' + self.get_full_name()
        temp_file = open(file_name, 'w')
        temp_file.close()
