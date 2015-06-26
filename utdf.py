# Matthew Bond
# A class for working with UTDF (Universal Traffic Data Format) files

import csv
import re

class Section():
    def __init__(self):
        self.data = []
        self.col_names = []
        self.row_names = []

    def add_value(self, c_name, r_name, value):
        if r_name not in self.row_names:
            self.row_names.append(r_name)
            self.data.append([None] * len(self.col_names))
        if c_name not in self.col_names:
            self.col_names.append(c_name)
            for row in self.data:
                row.append(None)
        x = self.row_names.index(r_name)
        y = self.col_names.index(c_name)
        self.data[x][y] = value

    def get_diff_cols(self, other):
        self_set, other_set = set(self.col_names), set(other.col_names)
        return (self_set - other_set), (other_set - self_set)

    def get_diff_rows(self, other):
        self_set, other_set = set(self.row_names), set(other.row_names)
        return (self_set - other_set), (other_set - self_set)

    def diff(self, other):
        pass

class UTDF():
    def __init__(self, f_path=None):
        self.sections = {}
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
                        s_name = match.group(1)
                        self.sections[s_name] = Section()
                        headers = []
                elif headers == []:
                    headers = row[1:]
                else:
                    for c_name, value in zip(headers, row[1:]):
                        self.sections[s_name].add_value(c_name, row[0], value)
