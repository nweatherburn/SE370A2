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

    def _is_directory(self):
        return self.directory

    def _is_file(self):
        return not self._is_directory()

    def _get_name(self):
        return self.name

    def get_full_name(self):
        if self.parent:
            full_name = self.parent.get_full_name() + self._get_name()
            if self._is_directory():
                full_name += Constants.DIRECTORY_DIVIDER
            return full_name
        else:
            return Constants.ROOT

    def _get_file_name(self):
        return Constants.DIRECTORY_NAME + '/' + self.get_full_name()

    def add_file(self, filename, create_file=True):
        path = filename.split(Constants.DIRECTORY_DIVIDER)
        self._add_file(path, create_file)

    def _add_file(self, path, create_file):
        if len(path) == 1:
            # Is file
            self.children[path[0]] = FileTrie(path[0], False, self)
            if create_file:
                self.children[path[0]]._create_as_file()
        else:
            if path[0] in self.children:
                child = self.children[path[0]]
            else:
                child = FileTrie(path[0], True, self)
                self.children[path[0]] = child
            child._add_file(path[1:], create_file)

    def get_parent(self):
        return self.parent

    def get_file(self, file_name):
        path = file_name.split(Constants.DIRECTORY_DIVIDER)

        f = self._get_child(path)
        assert f._is_file()
        return f

    def get_directory(self, directory_name):
        path = directory_name.split(Constants.DIRECTORY_DIVIDER)
        if len(path) > 0 and path[-1] == '':
            del path[-1]

        dir = self._get_child(path)
        assert dir._is_directory()
        return dir

    def _get_child(self, path):
        if len(path) == 0:
            # We're in directory
            return self
        else:
            return self.children[path[0]]._get_child(path[1:])

    def _create_as_file(self):
        file_name = self._get_file_name()
        temp_file = open(file_name, 'w')
        temp_file.close()

    def list_files(self):
        for name, child in sorted(self.children.items()):
            if child._is_file():
                print("f:", name)
            elif child._is_directory():
                print("d:", name)

    def tree(self, depth=0):
        self._print_self(depth)

        for name, child in sorted(self.children.items()):
            if child._is_directory():
                child.tree(depth + 1)
            elif child._is_file():
                child.tree(depth)

    def _print_self(self, depth=0):
        if self._is_directory():
            name = self.get_full_name()
            print(Constants.INDENT * depth + name)
            print(Constants.INDENT * depth + '=' * len(name))
        else:
            print(Constants.INDENT * depth + self._get_name())

    def delete(self):
        if self._is_directory():
            self._delete_directory()
        elif self._is_file():
            self._delete_file()

        if self.parent:
            self.parent._delete_child(self._get_name())

    def _delete_directory(self):
        for name, child in self.children.items():
            if child._is_directory():
                child._delete_directory()
            elif child._is_file():
                child._delete_file()

        self.children = {}

    def _delete_file(self):
        file_name = self._get_file_name()
        os.remove(file_name)

    def _delete_child(self, child_name):
        del self.children[child_name]

    def append(self, text):
        assert self._is_file()
        with open(self._get_file_name(), 'a') as f:
            f.write(text)

    def cat(self):
        assert self._is_file()
        with open(self._get_file_name(), 'r') as f:
            print(f.read())
