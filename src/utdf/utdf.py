# Matthew Bond
# Comparing and analyzing UTDF sqlite dbs


import sqlite3


def compare(results, key=None):
    union, intersection = set(), None
    for db_path in results:
        if key is not None:
            results[db_path] = [row[key] for row in results[db_path]]
        union = union | set(results[db_path])
        if intersection is None:
            intersection = set(results[db_path])
        intersection = intersection & set(results[db_path])
    for db_path in results:
        results[db_path] = set(results[db_path]) - intersection
    return union, intersection, results


def compare_nodes(*args):
    cmd, results = 'SELECT intid, type, x, y, z FROM Nodes', {}
    for db_path in args:
        results[db_path] = []
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute(cmd)
        for row in cur.fetchall():
            results[db_path].append(row)
        conn.close()
    return compare(results, None)
