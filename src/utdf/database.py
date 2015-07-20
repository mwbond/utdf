# Matthew Bond
# Building a sqlite db from UTDF (Universal Traffic Data Format) csv files

import csv

import utdf.definition


# Yields section_name, col_names, data for each section in the UTDF csv file
def get_data(csv_path):
    section_name, col_names, data = None, None, []
    with open(csv_path, 'r', newline='') as csv_file:
        for row in csv.reader(csv_file):
            if not row:
                yield section_name, col_names, data
                section_name, col_names, data = None, None, []
            elif len(row) == 1:
                if row[0].strip('[]') in utdf.definition.TABLES:
                    section_name = row[0].strip('[]')
            elif col_names is None:
                col_names = row
            else:
                data.append(row)
    if section_name and col_names and data:
        yield section_name, col_names, data


# Builds a table and inserts the data
def add_section(cur, table, dict_data):
    table_def = utdf.definition.TABLES[table]
    columns = ', '.join(['{} {}'.format(*col) for col in table_def])
    cur.execute('CREATE TABLE IF NOT EXISTS {} ({})'.format(table, columns))
    for row in dict_data:
        keys, values = zip(*row.items())
        columns = ', '.join([name.lower().replace(' ', '_') for name in keys])
        marks = ', '.join(['?'] * len(values))
        cmd = 'INSERT INTO {} ({}) VALUES ({})'.format(table, columns, marks)
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


def add_csv(cur, csv_path):
    print(csv_path)
    f_name = input('What f_name for this file? ') or csv_path
    print()
    for section_name, col_names, data in get_data(csv_path):
        if section_name == 'Nodes':
            dict_data = [dict(zip(col_names, row)) for row in data]
        else:
            if section_name == 'Network':
                dict_data = [dict(data)]
            else:
                dict_data = transpose(col_names, data)
        for row in dict_data:
            row['f_name'] = f_name
        add_section(cur, section_name, dict_data)


def create(cur, csv_paths=None):
    if csv_paths is None:
        csv_paths = []
    for table in utdf.definition.TABLES:
        cur.execute('DROP TABLE IF EXISTS {}'.format(table))
    for path in csv_paths:
        add_csv(cur, path)


def save_table_to_csv(cur, table):
    csv_path = '{}.csv'.format(table)
    cur.execute('SELECT * FROM {}'.format(table))
    with open(csv_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([row[0] for row in cur.description])
        writer.writerows(cur.fetchall())
