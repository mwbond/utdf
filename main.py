# Matthew Bond
# A main test class

import os

import utdf


def main():
    folder = 'Data'
    for f_name in os.listdir(folder):
        if f_name[-4:] == '.csv':
            f_path = os.path.join(folder, f_name)
            db_path = f_path[:-3] + 'db'
            attributes = utdf.build_db(db_path, f_path)
            u = utdf.UTDF(db_path, attributes)
            print(u.correct_version())
            utdf.save_table_to_csv(db_path, 'Phases')

if __name__ == '__main__':
    main()
