# Matthew Bond
# Building a sqlite db from UTDF (Universal Traffic Data Format) csv files

import csv
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
                if (row[0][0] == '[') and (row[0][-1] == ']'):
                    section_name = row[0].strip('[]')
            elif col_names is None:
                col_names = row
            else:
                data.append(row)
    if section_name and col_names and data:
        yield section_name, col_names, data


def build_cmds(table_name, col_names, sql_types):
    col_names = [name.lower().replace(' ', '_') for name in col_names]
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


def transpose(col_names, data, col_desc):
    headers, t_data = [], {}
    for row in data:
        if row[0] not in headers:
            headers.append(row[0])
    for row in data:
        name, intid = row[:2]
        index = headers.index(name)
        for col, value in zip(col_names[2:], row[2:]):
            if (intid, col) not in t_data:
                t_data[(intid, col)] = [''] * len(headers)
            t_data[(intid, col)][index] = value
    data = []
    headers = ['INTID'] + headers
    if col_desc is not None:
        headers.append(col_desc)
    for intid, col in t_data:
        if any(t_data[(intid, col)]):
            if col_desc is not None:
                t_data[(intid, col)].append(col)
            data.append([intid] + t_data[(intid, col)])
    return headers, data


def build_db(db_path, f_path):
    for section_name, col_names, data in get_data(f_path):
        unique = False
        if section_name == 'Network':
            col_names, data = zip(*data)
            data = [data]
        elif section_name == 'Nodes':
            unique = True
        else:
            col_desc = 'direction'
            if section_name == 'Phases':
                col_desc = 'phase'
            elif section_name == 'Timeplans':
                col_desc = None
            col_names, data = transpose(col_names, data, col_desc)
        build_table(db_path, section_name, col_names, data, unique)


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
