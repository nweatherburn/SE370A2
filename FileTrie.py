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
import os


class FileTrie(object):
    def __init__(self, name, is_directory, parent):
        self.name = name
        self.directory = is_directory
        self.children = {}
        self.parent = parent

    def is_directory(self):
        return self.directory

    def is_file(self):
        return not self.is_directory()

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

    def add_file(self, filename, create_file=True):
        path = filename.split(Constants.DIRECTORY_DIVIDER)
        self._add_file(path, create_file)

    def _add_file(self, path, create_file):
        if len(path) == 1:
            # Is file
            self.children[path[0]] = FileTrie(path[0], False, self)
            self.children[path[0]]._create_as_file()
        else:
            if path[0] in self.children:
                child = self.children[path[0]]
            else:
                child = FileTrie(path[0], True, self)
                self.children[path[0]] = child
            if create_file:
                child._add_file(path[1:])

    def get_parent(self):
        return self.parent

    def get_file(self, file_name):
        self.get_directory(file_name)

    def get_directory(self, directory_name):
        path = directory_name.split(Constants.DIRECTORY_DIVIDER)
        if len(path) > 0 and path[-1] == '':
            del path[-1]

        return self._get_directory(path)

    def _get_directory(self, path):
        if len(path) == 0:
            # We're in directory
            return self
        else:
            return self.children[path[0]]._get_directory(path[1:])

    def _create_as_file(self):
        file_name = Constants.DIRECTORY_NAME + '/' + self.get_full_name()
        temp_file = open(file_name, 'w')
        temp_file.close()

    def list_files(self):
        for name, child in sorted(self.children.items()):
            if child.is_file():
                print("f:", name)
            else:
                print("d:", name)

    def tree(self, depth=0):
        self.print_self(depth)

        for name, child in sorted(self.children.items()):
            if child.is_directory():
                child.tree(depth + 1)
            else:
                child.tree(depth)

    def print_self(self, depth=0):
        if self.is_directory():
            name = self.get_full_name()
            print(Constants.INDENT * depth + name)
            print(Constants.INDENT * depth + '=' * len(name))
        else:
            print(Constants.INDENT * depth + self.get_name())

    def delete(self):
        if self.is_directory():
            self._delete_directory()
        elif self.is_file():
            self._delete_file()

        if self.parent:
            self.parent._delete_child(self.get_name())

    def _delete_directory(self):
        assert self.is_directory()
        for name, child in self.children.items():
            child.delete()

    def _delete_file(self):
        file_name = Constants.DIRECTORY_NAME + '/' + self.get_full_name()
        os.remove(file_name)

    def _delete_child(self, child_name):
        del self.children[child_name]
