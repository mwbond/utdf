# Matthew Bond
# A main test class

import os

# import chart
import utdf.database
import utdf.utdf


def main():
    folder = os.path.join(os.pardir, 'data')
    db_path = os.path.join(folder, 'utdf.db')
    for f_path in os.listdir(folder):
        f_path = os.path.join(folder, f_path)
        if f_path[-4:] == '.csv':
            print(f_path)
            f_name = input('What f_name for this file? ')
            print()
            utdf.database.add_csv_to_db(db_path, f_path, f_name)
    utdf.database.save_table_to_csv(db_path, 'Network')
    utdf.database.save_table_to_csv(db_path, 'Nodes')
    utdf.database.save_table_to_csv(db_path, 'Links')
    utdf.database.save_table_to_csv(db_path, 'Lanes')
    utdf.database.save_table_to_csv(db_path, 'Timeplans')
    utdf.database.save_table_to_csv(db_path, 'Phases')


if __name__ == '__main__':
    main()
