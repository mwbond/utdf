# Matthew Bond
# Building a sqlite db from UTDF (Universal Traffic Data Format) csv files

import csv
import sqlite3


# Yields section_name, col_names, data for each section in the UTDF csv file
def get_data(csv_path):
    section_name, col_names, data = None, None, []
    with open(csv_path, 'r', newline='') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if not row:
                yield section_name, col_names, data
                section_name, col_names, data = None, None, []
            elif len(row) == 1:
                if (row[0][0] == '[') and (row[0][-1] == ']'):
                    section_name = row[0].strip('[]')
            elif col_names is None:
                col_names = row
            else:
                data.append(row)
    if section_name and col_names and data:
        yield section_name, col_names, data


def sanitize_col_name(col_name):
    return col_name.lower().replace(' ', '_')


# insert_cmd = 'INSERT INTO {} VALUES ({})'.format(table_name, values)
# Builds a table and inserts the data
def add_section(cur, table_name, col_names, dict_data):
    col_names = [sanitize_col_name(name) for name in col_names]
    columns = ', '.join(['{} {}'.format(col, 'TEXT') for col in col_names])
    cmd = 'CREATE TABLE IF NOT EXISTS {} ({})'.format(table_name, columns)
    cur.execute(cmd)
    cur.execute('SELECT * FROM {}'.format(table_name))
    existing = [col[0] for col in cur.description]
    for col in set(col_names) - set(existing):
        cmd = 'ALTER TABLE {} ADD COLUMN {} TEXT'.format(table_name, col)
        cur.execute(cmd)
    for row in dict_data:
        keys, values = zip(*row.items())
        keys = ', '.join([sanitize_col_name(name) for name in keys])
        marks = ', '.join(['?'] * len(values))
        cmd = 'INSERT INTO {} ({}) VALUES ({})'.format(table_name, keys, marks)
        cur.execute(cmd, values)


# Transposes the data such that the first column in each row (RECORDNAME) is
# set as a column, and each column name is set as an additional row value
def transpose(col_names, data):
    t_data = {}
    for row in data:
        recordname, intid = row[:2]
        for name, value in zip(col_names[2:], row[2:]):
            if value:
                if (intid, name) not in t_data:
                    t_data[(intid, name)] = {'intid': intid}
                    if name != 'DATA':
                        t_data[(intid, name)]['direction'] = name
                t_data[(intid, name)][recordname] = value
    return t_data.values()


def add_csv_to_db(db_path, csv_path, f_name=None):
    if f_name is None:
        f_name = csv_path
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    for section_name, col_names, data in get_data(csv_path):
        db_col_names = ['f_name']
        if section_name == 'Nodes':
            db_col_names.extend(col_names)
            dict_data = [dict(zip(col_names, row)) for row in data]
        else:
            if section_name == 'Network':
                dict_data = [dict(data)]
            else:
                dict_data = transpose(col_names, data)
                db_col_names.append('intid')
            if 'DATA' not in col_names:
                db_col_names.append('direction')
            db_col_names.extend(set([row[0] for row in data]))
        for row in dict_data:
            row['f_name'] = f_name
        add_section(cur, section_name, db_col_names, dict_data)
    conn.commit()
    conn.close()


def save_table_to_csv(db_path, table_name):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('SELECT * FROM ' + table_name)
    csv_path = db_path[:-3] + '_' + table_name + '.csv'
    with open(csv_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([row[0] for row in cur.description])
        for row in cur.fetchall():
            writer.writerow(row)
    conn.close()
