# Matthew Bond
# A simple class for easy output of charts

class Chart():
    def __init__(self, headers_rpt=30):
        if rows is None:
            rows = []
        self.headers_rpt = headers_rpt
        self.rows =  rows
        self.widths = []

    def create_line(self, r):
        line = []
        for w, cell in zip(self.widths, r):
            line.append(cell.ljust(w, ' '))
        return ' | '.join(line)

    def output(self):
        self.update_widths()
        table_width = sum(self.widths) + 3 * (len(self.widths) - 1)
        for count, r in enumerate(self.rows[1:]):
            if count % self.headers_rpt == 0:
                print('-' * table_width)
                print(self.create_line(self.rows[0]))
                print('-' * table_width)
            print(self.create_line(r))

    def update_widths(self):
        self.widths = [max(map(len, column)) for column in zip(*self.rows)]
