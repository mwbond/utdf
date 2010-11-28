# Matthew Bond
# Nov 26, 2010
# pprinter.py

def pprinter(headers, values):
	paddedHeaders = []
	paddedValuesList = []
	dividers = []
	dblDividers = []

	for col_text in zip(headers, *values):
		paddedValues = []
		columnWidth = max([len(text) for text in col_text])
		paddedHeaders.append(col_text[0].center(columnWidth))
		for text in col_text[1:]:
			paddedValues.append(text.center(columnWidth))
		paddedValuesList.append(paddedValues)
		dividers.append('-' * columnWidth)
		dblDividers.append('=' * columnWidth)

	print '+-' + '-+-'.join(dividers) + '-+'
	print '| ' + ' | '.join(paddedHeaders) + ' |'
	for paddedValues in zip(*paddedValuesList):
		print '+=' + '=+='.join(dblDividers) + '=+'
		print '| ' + ' | '.join(paddedValues) + ' |'
		print '+-' + '-+-'.join(dividers) + '-+'

