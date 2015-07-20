# Matthew Bond
# A main test class

import os
import sqlite3

# import chart
import utdf.database
# import utdf.utdf


def main():
    folder = os.path.join(os.pardir, 'data')
    csv_paths = []
    for f_name in os.listdir(folder):
        if f_name[-4:] == '.csv':
            csv_paths.append(os.path.join(folder, f_name))
    db_path = os.path.join(folder, 'utdf.db')
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    utdf.database.create(cur, csv_paths)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    main()
