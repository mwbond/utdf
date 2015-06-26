# Matthew Bond
# A class for working with UTDF (Universal Traffic Data Format) files

import collections
import csv
import re

class UTDF():
    def __init__(self, f_path=None):
        self.data = collections.OrderedDict()
        if f_path is not None:
            self.build(f_path)

    def build(self, f_path):
        self.data = {}
        headers, section = [], 'None'
        section_re = re.compile('\[(.+)\]')
        with open(f_path, 'r', newline='') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if not row:
                    pass
                elif len(row) == 1:
                    match = section_re.fullmatch(row[0])
                    if match:
                        section = match.group(1)
                        self.data[section] = collections.OrderedDict()
                        headers = []
                elif headers == []:
                    headers = row[1:]
                    for col_name in headers:
                        self.data[section][col_name] = {}
                else:
                    self.data[section][row[0]] = collections.OrderedDict()
                    for col_name, value in zip(headers, row[1:]):
                        self.data[section][row[0]][col_name] = value

    def find_all(self, section=None, row_name=None, col_name=None):
        for s in self.data:
            if (section is None) or (s == section):
                for r in self.data[s]:
                    if (row_name is None) or (r == row_name):
                        for c in self.data[s][r]:
                            if (col_name is None) or (c == col_name):
                                yield s, r, c

    def find_added(self, other, **kwargs):
        for s, r, c in other.find_all(**kwargs):
            try:
                original = self.data[s][r][c]
            except KeyError:
                yield s, r, c


    def find_removed(self, other, **kwargs):
        for s, r, c in self.find_all(**kwargs):
            try:
                new = other.data[s][r][c]
            except KeyError:
                yield s, r, c

    def find_changed(self, other, **kwargs):
        for s, r, c in self.find_all(**kwargs):
            try:
                new = other.data[s][r][c]
            except KeyError:
                pass
            else:
                if self.data[s][r][c] != new:
                    yield s, r, c

    def find_unchanged(self, other, **kwargs):
        for s, r, c in self.find_all(**kwargs):
            try:
                new = other.data[s][r][c]
            except KeyError:
                pass
            else:
                if self.data[s][r][c] == new:
                    yield s, r, c
