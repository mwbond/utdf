# Matthew Bond
# A main test class

import os

import chart
import utdf

def main():
    folder = 'Data'
    old, new = None, None
    for f_name in os.listdir(folder):
        if f_name[-4:] == '.csv':
            f_path = os.path.join(folder, f_name)
            db_path = f_path[:-3] + 'db'
            network = utdf.UTDF(db_path, f_path)
            break
            '''if old is not None:
                for key in new.sections:
                    a = new.sections[key]
                    b = old.sections[key]
                    output = a.diff_rows(b)
                    if any(output):
                        print(a.row_names)
                        print(b.row_names)
                        print(output)
                        input('Press Enter')'''
            old = new

if __name__ == '__main__':
    main()
