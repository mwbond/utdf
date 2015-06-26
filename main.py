# Matthew Bond
# A main test class

import os

import chart
import utdf

def output(section):
    s_chart = chart.Chart()
    s_chart.rows.append([''] + section.col_names)
    for r_name, row in zip(section.row_names, section.data):
        s_chart.rows.append([r_name] + row)
    s_chart.output()

def main():
    folder = 'Data'
    old, new = None, None
    for f_name in os.listdir(folder):
        if f_name[-4:] == '.csv':
            f_path = os.path.join(folder, f_name)
            new = utdf.UTDF(f_path)
            if old is not None:
                for key in new.sections:
                    a = new.sections[key]
                    b = old.sections[key]
                    output = a.diff_rows(b)
                    if any(output):
                        print(a.row_names)
                        print(b.row_names)
                        print(output)
                        input('Press Enter')
            old = new

if __name__ == '__main__':
    main()
