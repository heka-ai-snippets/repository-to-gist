# !/usr/bin/env python
# -*- coding: utf-8 -*-


"""
Classes & functions related to file management
"""


# =========================================================================================================
# ================================ 0. MODULE


import os
from glob import glob

import hashlib


# =========================================================================================================
# ================================ 1. CLASSES


class FilesManager(object):
    def __init__(self, path=None):
        """_summary_

        Parameters
        ----------
        path : str, optional
            Path of the files to manage, by default None
        """
        self.path = os.getcwd() if path is None else path
        print(f'Linked to {self.path}')

    def list_files(self, get_checksum=False):
        """_summary_

        Returns
        -------
        List[str]
            List of relative paths
        """
        print(f'Listing files in {self.path}')
        files = glob(f'{self.path}/**/*.*', recursive=True)
        file_names = [f.split(self.path)[1] for f in files]
        if get_checksum:
            checksums = [hashlib.md5(self.get_file(f, binary=True)).hexdigest() for f in file_names]
            return list(zip(file_names, checksums))
        else:
            return file_names

    def get_file(self, relative_path, binary=False):
        """Collect the content of a file as a string

        Parameters
        ----------
        relative_path : str
            Relative path of the file to retrieve

        Returns
        -------
        str
            Content of the file
        """
        format = 'rb' if binary else 'r'
        with open(f'{self.path}/{relative_path}', format) as file:
            return file.read()
