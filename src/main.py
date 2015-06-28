# Matthew Bond
# A main test class

import os

import utdf.build


def main():
    folder = os.path.join(os.pardir, 'data')
    for f_name in os.listdir(folder):
        if f_name[-4:] == '.csv':
            f_path = os.path.join(folder, f_name)
            db_path = f_path[:-3] + 'db'
            print(db_path)
            utdf.build.build_db(db_path, f_path)
            utdf.build.save_table_to_csv(db_path, 'Network')

if __name__ == '__main__':
    main()
