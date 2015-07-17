# Matthew Bond
# Building a sqlite db from UTDF (Universal Traffic Data Format) csv files

import csv
import sqlite3


FORMAT = {'Network': ['f_name', 'utdfversion', 'metric', 'yellowtime',
                      'allredtime', 'walk', 'dontwalk', 'hv', 'phf',
                      'defwidth', 'defflow', 'vehlength', 'heavyvehlength',
                      'criticalgap', 'followuptime', 'stopthresholdspeed',
                      'criticalmergegap', 'growth', 'pedspeed',
                      'losttimeadjust', 'scenariodate', 'scenariotime'],
          'Nodes': ['f_name', 'intid', 'type', 'x', 'y', 'z', 'description',
                    'cbd', 'inside_radius', 'outside_radius',
                    'roundabout_lanes', 'circle_speed'],
          'Links': ['f_name', 'intid', 'time', 'speed', 'twltl',
                    'link_is_hidden', 'lanes', 'up_id',
                    'positioning_distance2', 'distance', 'curve_pt_z',
                    'street_name_is_hidden', 'mandatory_distance',
                    'mandatory_distance2', 'positioning_distance', 'median',
                    'offset', 'curve_pt_y', 'crosswalk_width', 'curve_pt_x',
                    'grade', 'name', 'direction'],
          'Lanes': ['f_name', 'intid', 'idealflow', 'bicycles', 'detectphase4',
                    'detectextend1', 'right_radius', 'lanes', 'signcontrol',
                    'detectsize2', 'taper', 'traffic_in_shared_lane',
                    'distance', 'add_lanes', 'peds', 'detectphase2',
                    'allow_rtor', 'satflow', 'heavyvehicles', 'lastdetect',
                    'midblock', 'speed', 'detectqueue1', 'phase1',
                    'lane_group_flow', 'numdetects', 'traveltime',
                    'detectphase3', 'headwayfact', 'busstops', 'phf',
                    'detectphase1', 'detectextend2', 'cbd', 'satflowrtor',
                    'turning_speed', 'alignment', 'losttime', 'switchphase',
                    'stlanes', 'dest_node', 'detectdelay1', 'firstdetect',
                    'detectpos2', 'width', 'exit_lanes', 'detectsize1',
                    'up_node', 'storage', 'volume', 'enter_blocked', 'growth',
                    'detecttype1', 'shared', 'lost_time_adjust',
                    'detecttype2', 'satflowperm', 'grade', 'right_channeled',
                    'permphase1', 'detectpos1', 'direction'],
          'Timeplans': ['f_name', 'intid', 'lock_timings', 'control_type',
                        'cycle_length', 'node_0', 'yield', 'referenced_to',
                        'master', 'node_1', 'offset', 'reference_phase'],
          'Phases': ['f_name', 'intid', 'vehext', 'minsplit', 'yield', 'brp',
                     'timebeforereduce', 'mingap', 'end', 'localstart',
                     'timetoreduce', 'inhibitmax', 'pedcalls', 'dontwalk',
                     'localyield170', 'maxgreen', 'yield170', 'actgreen',
                     'walk', 'yellow', 'mingreen', 'allred', 'dualentry',
                     'localyield', 'recall', 'start', 'direction']}


# Yields section_name, col_names, data for each section in the UTDF csv file
def get_data(csv_path):
    section_name, col_names, data = None, None, []
    with open(csv_path, 'r', newline='') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            if not row:
                yield section_name, col_names, data
                section_name, col_names, data = None, None, []
            elif len(row) == 1:
                if (row[0][0] == '[') and (row[0][-1] == ']'):
                    section_name = row[0].strip('[]')
            elif col_names is None:
                col_names = row
            else:
                data.append(row)
    if section_name and col_names and data:
        yield section_name, col_names, data


# Transposes the data such that the first column in each row (RECORDNAME) is
# set as a column, and each column name is set as an additional row value
# unless the column name is DATA
def transpose(col_names, data):
    headers, t_data, ignore = list(set(next(zip(*data)))), {}, 'DATA'
    for row in data:
        recordname, intid = row[:2]
        index = headers.index(recordname)
        for name, value in zip(col_names[2:], row[2:]):
            if (intid, name) not in t_data:
                t_data[(intid, name)] = [None] * len(headers)
            t_data[(intid, name)][index] = value
    data = []
    headers = ['INTID'] + headers
    if col_names[-1] != ignore:
        headers.append('DIRECTION')
    for (intid, name), row in t_data.items():
        if any(row):
            row = [intid] + row
            if name != ignore:
                row.append(name)
            data.append(row)
    return headers, data


def add_csv_to_db(db_path, csv_path, f_name=None):
    if f_name is None:
        f_name = csv_path
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    for section_name, col_names, data in get_data(csv_path):
        if section_name == 'Network':
            col_names, data = zip(*data)
            data = [data]
        elif section_name != 'Nodes':
            col_names, data = transpose(col_names, data)
        insert_cmd = 'INSERT INTO {} VALUES ({})'.format(table_name, values)
        for row in data:
            row = (f_name,) + tuple(row)
            cur.execute(insert_cmd, row)
    conn.commit()
    conn.close()


def save_table_to_csv(db_path, table_name):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('SELECT * FROM ' + table_name)
    csv_path = db_path[:-3] + '_' + table_name + '.csv'
    with open(csv_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([row[0] for row in cur.description])
        for row in cur.fetchall():
            writer.writerow(row)
    conn.close()

col_names = name.lower().replace(' ', '_')
