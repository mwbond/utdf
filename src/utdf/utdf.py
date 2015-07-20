# Matthew Bond
# Comparing and analyzing UTDF sqlite dbs

from decimal import Decimal


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


def whole_number(num):
    return int(num) == num


def whole_splits(maxgreen, yellow, allred):
    return whole_number(maxgreen + yellow + allred)


def minimum_green(mingreen, yellow, allred, minsplit, green_time=5):
    min_split_green = minsplit - yellow - allred
    if (mingreen < green_time) or (min_split_green < green_time):
        return False
    return True


def check_phases(cur):
    identifiers = ['f_name', 'intid', 'direction']
    values = ['mingreen', 'maxgreen', 'yellow', 'allred', 'minsplit']
    for row in query_db(cur, 'Phases', identifiers + values):
        try:
            min_g, max_g, y, ar, min_s = [Decimal(row[key]) for key in values]
        except ValueError:
            yield 'Value Error', row
        except TypeError:
            yield 'Type Error', row
        else:
            if not whole_splits(max_g, y, ar):
                yield 'Whole Split Error', row
            if not minimum_green(min_g, y, ar, min_s, 4):
                yield 'Low Green Error', row


def check_timeplans(cur):
    identifiers = ['f_name', 'intid']
    values = ['cycle_length']
    for row in query_db(cur, 'Timeplans', identifiers + values):
        try:
            cycle_length, = [Decimal(row[key]) for key in values]
        except ValueError:
            yield 'Value Error', row
        except TypeError:
            yield 'Type Error', row
        else:
            if not whole_number(cycle_length):
                yield 'Whole Cycle Error', row


# Returns [intid, (x, y, z), set(link names)]
def get_nodes_information(cur, node_type=None):
    results, where = [], None
    if node_type in map(str, range(5)):
        where = {'type': node_type}
    for row in query_db(cur, 'Nodes', ['intid', 'x', 'y', 'z'], where):
        row = [row[0], row[1:], set()]
        for names in query_db(cur, 'Links', ['name'], {'intid': row[0]}):
            row[2] = row[2] | set(names)
        results.append(row)
    return results


'''def match_signal_locations(cur):
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
    return results'''
