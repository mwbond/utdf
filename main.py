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
            new = utdf.UTDF(f_path)
            if old is not None:
                ch = chart.Chart()
                ch.rows.append(['Section', 'Row', 'Column', 'Old', 'New'])
                for s, c, r in new.find_changed(old, section='Nodes'):
                    r = [s, c, r, old.data[s][c][r], new.data[s][c][r]]
                    ch.rows.append(r)
                ch.output()
                input()
            old = new

if __name__ == '__main__':
    main()
