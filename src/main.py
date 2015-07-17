# Matthew Bond
# A main test class

import os

import chart
import utdf.build
import utdf.utdf

ORIG_PATH_DB = 'US 29_RIO GSI_2015_AM_Phase-1B Day.db'
ORIG_PATH_CSV = 'US 29_RIO GSI_2015_AM_Phase-1B Day.csv'
COMP_PATH = 'US 29_RIO GSI_2015_Phase-1 Night.db'
# COMP_PATH = 'US 29_RIO GSI_2015_AM_Phase-1B Day.db'


def main():
    folder = os.path.join(os.pardir, 'data')
    for f_path in os.listdir(folder):
        db_path = os.path.join(folder, f_path)
        '''if db_path[-3:] == '.db':
            print(db_path)
            utdf.utdf.check_phases(db_path)'''
        if db_path[-4:] == '.csv':
            csv_path = db_path
            db_path = csv_path[:-4] + '.db'
            utdf.build.build_db(csv_path, db_path)
            break


if __name__ == '__main__':
    main()
