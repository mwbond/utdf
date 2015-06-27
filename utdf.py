# Matthew Bond
# A class for working with UTDF (Universal Traffic Data Format) files

import csv
import re
import sqlite3

def get_data(f_path):
    section_name, col_names, data = None, None, []
    with open(f_path, 'r', newline='') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if not row:
                yield section_name, col_names, data
                section_name, col_names, data = None, None, []
            elif len(row) == 1:
                match = table_re.fullmatch(row[0])
                if match:
                    section_name = match.group(1)
            elif col_names is None:
                col_names = row
            else:
                data.append(row)

def build_cmds(table_name, col_names, sql_types):
    col_names = [name.lower().replace(' ', '_')  for name in col_names]
    columns = ', '.join([' '.join(col) for col in zip(col_names, sql_types)])
    create_cmd = 'CREATE TABLE ' + table_name + ' (' + columns + ')'
    insert_cmd = 'INSERT INTO ' + table_name + ' VALUES ('
    insert_cmd += ', '.join(['?'] * len(col_names)) + ')'
    return create_cmd, insert_cmd

def build_table(db_path, table_name, col_names, data, unique=False):
    sql_types = ['TEXT'] * len(col_names)
    if unique:
        sql_types[0] += ' UNIQUE'
    create_cmd, insert_cmd = build_cmds(table_name, col_names, sql_types)
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('DROP TABLE IF EXISTS ' + table_name)
    cur.execute(create_cmd)
    for row in data:
        cur.execute(insert_cmd, tuple(row))
    conn.commit()
    conn.close()

def build_db(db_path, f_path):
    attributes = {}
    for section_name, col_names, data in get_data(f_path):
        if section_name == 'Network':
            for key, value in zip(*data):
                attributes[key] = value
        elif section_name == 'Network':
            build_table(section_name, col_names, data, True)
        else:
            pass
    return attributes

class UTDF():
    UTDF_VERSION = '8'
    def __init__(self, db_path, f_path=None):
        self.db = db_path
        if f_path is not None:
            build_db(db_path, f_path)

    def correct_version(self):
        return True
