# Matthew Bond
# A simple class for easy output of charts

class Chart():
    def __init__(self, data=None):
        self.data = []
        self.widths = []
        self.add_data(data)
        self.has_col_names, self.has_row_names = False, False

    def add_data(self, data):
        for row in data:
            self.data.append(row)

    def add_labels(self, col_names=None, row_names=None):
        if col_names is not None:
            for row in self.data:
                if len(row) == len(col_names):
                    self.data = [col_names] + self.data
                    self.has_col_names = True
                    row_names = [''] + row_names
        if (row_names is not None) and (len(self.data) == len(row_names)):
            for row, name in zip(self.data, row_names):
                row = [name] + row
            self.has_row_names = True

    def get_line(self, r):
        line = []
        for w, cell in zip(self.widths, r):
            line.append(cell.ljust(w, ' '))
        if self.has_row_name:
            return line + ' || ' + ' | '.join(line[1:])
        return ' | '.join(line)

    def get_headers(self):
        table_width = sum(self.widths) + 3 * (len(self.widths) - 1)
        sep = '-' * table_width
        headers = self.get_line(self.data[0])
        return '\n'.join([sep, headers, sep])

    def output(self, col_names_rpt=30):
        self.update_widths()
        for count, row in enumerate(self.data):
            if (self.has_col_names) and (count % col_names_rpt == 0):
                print(get_headers)
            if (not self.has_col_names) or (count != 0):
                print(self.create_line(row))

    def reset(self):
        self.data = []
        self.widths = []
        self.has_col_names, self.has_row_names = False, False

    def update_widths(self):
        self.widths = [max(map(len, column)) for column in zip(*self.data)]
