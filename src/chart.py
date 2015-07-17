# Matthew Bond
# A simple class for easy output of charts

class Chart():
    def __init__(self, data=None, col_names=None, row_names=None):
        data = data or []
        self.data = []
        for row in data:
            self.add_row(row)
        self.col_names = col_names or []
        self.row_names = row_names or []

    def add_row(self, row, name=None):
        row = [cell or '-' for cell in row]
        if self.data != []:
            self.adjust(row, len(self.data[0]))
        self.data.append(row)
        if (name is not None) or self.row_names:
            self.adjust(self.row_names, len(self.data))
            self.row_names[len(self.data) - 1] = name or ''

    def adjust(self, row, length):
        if len(row) < length:
            row.extend([''] * (length - len(row)))

    def get_line(self, row, widths):
        line = ['{!s:>{}}'.format(cell, w) for cell, w in zip(row, widths)]
        if self.row_names:
            return '{} || {}'.format(line[0], ' | '.join(line[1:]))
        return ' | '.join(line)

    def get_headers(self, col_names, widths):
        sep = '-' * (sum(widths) + 3 * (len(widths) - 1) + 1)
        if self.row_names:
            col_names = [''] + col_names
        return '\n'.join([sep, self.get_line(col_names, widths), sep])

    def matches_length(self, row):
        if self.data and (len(self.data[0]) != len(row)):
            return False
        return True

    def output(self, col_names_rpt=30):
        if self.col_names and self.data:
            self.adjust(self.col_names, len(self.data[0]))
        if self.row_names:
            self.adjust(self.row_names, len(self.data))
        widths = self.get_widths()
        for count, row in enumerate(self.data):
            if (self.col_names) and (count % col_names_rpt == 0):
                print(self.get_headers(self.col_names, widths))
            if self.row_names:
                row = [self.row_names[count]] + row
            print(self.get_line(row, widths))

    def reset(self):
        self.data, self.col_names, self.row_names = [], [], []

    def get_widths(self):
        widths = [max(map(len, map(str, row))) for row in zip(*self.data)]
        if self.col_names:
            col_widths = map(len, self.col_names)
            widths = [max(w) for w in zip(col_widths, widths)]
        if self.row_names:
            widths = [max(map(len, self.row_names))] + widths
        return widths
