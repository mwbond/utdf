# Matthew Bond
# Comparing and analyzing UTDF sqlite dbs


import sqlite3


# A wrapper for a db query
def query_db(cur, table_name, col_names=None, where=None):
    col_names = col_names or ['*']
    base_cmd = 'SELECT {} FROM {}'.format(', '.join(col_names), table_name)
    if where is not None:
        col_names, values = zip(*where.items())
        where_cmd = ' AND '.join(['{}=?'.format(name) for name in col_names])
        cur.execute('{} WHERE {}'.format(base_cmd, where_cmd), values)
    else:
        cur.execute(base_cmd)
    return cur.fetchall()


def whole_splits(max_g, yar):
    split = max_g + yar
    return int(split) == float(split)


def minimum_green(min_g, yar, min_s, green_time=4):
    min_split_green = minsplit - yellow - allred
    if (min_g <= green_time) or (min_s - yar <= green_time):
        return False
    return True


def check_phases(db_path):
    results = {}
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    col_names = ['intid', 'direction', 'mingreen', 'maxgreen', 'yellow',
                 'allred', 'minsplit']
    for row in query_db(cur, 'Phases', col_names):
        try:
            min_g, max_g, y, ar, min_s = [float(row[key]) for key in col_names]
        except ValueError:
            print('Error in reading', row['intid'], row['direction'])
        else:
            if not whole_splits(max_g, y + ar):
                print('Non-whole splits at', row['intid'], row['direction'])
            if not minimum_green(min_g, y + ar, min_s):
                print('Low green time at', row['intid'], row['direction'])
    conn.close()


# Returns [intid, (x, y, z), set(link names)] in db_path
def get_nodes_information(db_path, node_type=None):
    results, where = [], None
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    if node_type in map(str, range(5)):
        where = {'type': node_type}
    for row in query_db(cur, 'Nodes', ['intid', 'x', 'y', 'z'], where):
        row = [row[0], row[1:], set()]
        for names in query_db(cur, 'Links', ['name'], {'intid': row[0]}):
            row[2] = row[2] | set(names)
        results.append(row)
    conn.close()
    return results


def match_signal_locations(db_paths):
    results = {}
    for index, path in enumerate(db_paths):
        for intid, xyz, names in get_nodes_information(path):
            if xyz not in results:
                results[xyz] = [None] * len(db_paths)
            results[xyz][index] = intid
    return results


def match_dir_attrs(db_paths, table_name, recordname, intid):
    results = {}
    for index, path in enumerate(db_paths):
        col_names, where = ['direction', recordname], {'intid': intid}
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        for direction, value in query_db(cur, table_name, col_names, where):
            if direction not in results:
                results[direction] = [None] * len(db_paths)
            results[direction][index] = value
        conn.close()
    return results
