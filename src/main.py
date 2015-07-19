# Matthew Bond
# A main test class

import os
import sqlite3

# import chart
import utdf.database
import utdf.utdf


def main():
    folder = os.path.join(os.pardir, 'data')
    db_path = os.path.join(folder, 'utdf.db')
    for f_path in os.listdir(folder):
        f_path = os.path.join(folder, f_path)
        if f_path[-3:] == '.db':
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            for error, row in utdf.utdf.check_phases(cur):
                print(error, 'at', row['f_name'], row['intid'])
            conn.close()


if __name__ == '__main__':
    main()
