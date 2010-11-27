# Matthew Bond
# Nov 16, 2010
# utdf.py

import csv, pprinter

def getStrListSum(sum_list, start, end):
	num_list = sum_list[start:end + 1]
	for index in range(len(num_list)):
		if num_list[index] == "":
			num = 0
		else:
			num = int(num_list[index])
		num_list[index] = num
	return sum(num_list)

def readFile(filename, mode='r'):
	info = []
	csv_file = open(filename, mode)
	for line in csv_file:
		line = line.rstrip().split(",")
		if len(line) > 1:
			info.append(line)
	return csv_file, info

# ped_opt == True ignores pedestrian counts
# phf_opt == True ignores PHF
def getVolAnom(filename="LANES.CSV", ped_opt=False, phf_opt=False):
	col =[]
	int_ids = []
	csv_file, info = readFile(filename)
	try:
		record_index = info[0].index("RECORDNAME")
		id_index = info[0].index("INTID")
		for index in range(len(info[0])):
			if info[0][index][0] in ("N", "S", "E", "W"):
				col.append(index)
		start = col[0]
		end = col[-1]
	except (ValueError, IndexError):
		csv_file.close()
		return []
	info = [line for line in info if line[record_index] in ("Volume",
															"Peds",
															"PHF")]
	for index in range(len(info))[::3]:
		line = info[index]
		assert line[0] == "Volume"
		vol_sum = getStrListSum(line, start, end)
		line = info[index + 1]
		assert line[0] == "Peds"
		ped_sum = getStrListSum(line, start, end)
		line = info[index + 2]
		phf_change = False
		for phf in line[start:end + 1]:
			if phf not in ("", "0.92"):
				phf_change = True
				break
		if (vol_sum > 0) and ((ped_sum == 0) or ped_opt) and ((not phf_change) or phf_opt):
			int_ids.append(line[id_index])
	csv_file.close()
	return int_ids

def checkRounding(filename="VOLUME.CSV", change_vol=False, rounding_num=5):
	col =[]
	int_ids = []
	file_lines = []
	csv_file, info = readFile(filename, "r+")
	try:
		id_index = info[0].index("INTID")
		for index in range(len(info[0])):
			if info[0][index][0] in ("N", "S", "E", "W"):
				col.append(index)
		start = col[0]
		end = col[-1]
	except (ValueError, IndexError):
		csv_file.close()
		return []
	for line in info[1:]:
		for vol in line[start:end + 1]:
			if vol == "":
				vol_num = 0
			else:
				vol_num = int(vol)
			if vol_num % rounding_num != 0:
				int_ids.append(str(line[id_index]))
				break
	
	if not change_vol:
		csv_file.close()
		return int_ids
	csv_file.seek(0)
	info = csv_file.read().splitlines()
	for line in info:
		line = line.rstrip().split(",")
		try:
			if line[id_index] in int_ids:
				for index in range(start, end + 1):
					vol = line[index]
					if vol != "":
						vol_num = int(vol)
						line[index] = str((vol_num / rounding_num) * rounding_num
																		+ rounding_num)
			file_lines.append(",".join(line) + "\r\n")
		except (IndexError, ValueError):
			file_lines.append(",".join(line) + "\r\n")
	#file_text = "\r\n".join(file_lines) + 2 * "\r\n"
	#csv_file.write(file_text)
	csv_file.seek(0)
	csv_file.writelines(file_lines)
	csv_file.close()
	return int_ids

def intVolumeCheck(layout_filename="LAYOUT.CSV", lanes_filename="LANES.CSV"):
	layout_dict = {}
	lanes_dict = {}
	col = []
	values = []

	layout_file, layout_info = readFile(layout_filename)
	lanes_file, lanes_info = readFile(lanes_filename)

	layout_headers = layout_info.pop(0)
	lanes_headers = lanes_info.pop(0)

	for index in range(len(layout_headers)):
		if layout_headers[index][-4:] == "NAME":
			col.append(index)
	layout_start = col[1]
	layout_end = col[-1]
	for index in range(len(lanes_headers)):
		if lanes_headers[index][-4:] == "NAME":
			col.append(index)
	lanes_start = col[1]
	lanes_end = col[-1]

	for line in layout_info:
		layout_dict[line[0]] = line[1:]
	for line in lanes_info:
		lanes_dict[line[0]] = line[1:]

	while True:
		int_id = raw_input("Enter Intersection ID: ")
		if int_id == "":
			break
		try:
			layout_info = layout_dict[int_id]
			pprinter.pprinter(layout_headers, [[int_id] + layout_info])
		except KeyError:
			print "This Intersection ID is not in this file"

	lanes_file.close()
	layout_file.close()
