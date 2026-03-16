import pandas as pd
import json
import math
import sys
import os


def clean(v):
    if isinstance(v, float):
        if math.isnan(v):
            return None
        if v.is_integer():
            return int(v)
    if hasattr(v, 'item'):
        return v.item()
    return v


def convert(input_path, output_path=None):
    if not os.path.exists(input_path):
        print(f"Error: file '{input_path}' not found.")
        sys.exit(1)

    sheets = pd.read_excel(input_path, sheet_name=None)

    stations_df = sheets['stations']
    lines_df = sheets['lines']
    connections_df = sheets['connections']
    sl_df = sheets['station_line']
    joins_df = sheets['station_line_joins']

    # Build lines
    lines = {}
    for _, row in lines_df.iterrows():
        obj = {k: clean(v) for k, v in row.items()}
        lines[str(obj['id'])] = obj

    # Build connections lookup: station_line_id -> list
    conn_lookup = {}
    for _, row in connections_df.iterrows():
        sid = clean(row['station_line_id'])
        if sid is None:
            continue
        sid = int(sid)
        if sid not in conn_lookup:
            conn_lookup[sid] = []
        next_sl = clean(row['next_station_line_id'])
        line_id = clean(row['line'])
        conn_lookup[sid].append({
            'next_station_line_id': int(next_sl) if next_sl is not None else None,
            'line_id': int(line_id) if line_id is not None else None,
            'connection_style': str(row['connection_style'])
        })

    # Build joins lookup: station_line_id -> single join object (1-to-1)
    joins_lookup = {}
    for _, row in joins_df.iterrows():
        sid = int(row['station_line_id'])
        is_triplet = clean(row['is_triplet'])
        join_obj = {
            'position': str(row['position']),
            'offset': clean(row['offset']),
            'separate': bool(row['separate']),
        }
        if is_triplet is not None:
            join_obj['is_triplet'] = bool(is_triplet)
        joins_lookup[sid] = join_obj

    # Build stations — name_direction split by ";" into array
    stations = {}
    for _, row in stations_df.iterrows():
        obj = {}
        for k, v in row.items():
            if k == 'name_direction':
                raw = clean(v)
                if raw is None:
                    obj[k] = []
                else:
                    obj[k] = [d.strip() for d in str(raw).split(';') if d.strip()]
            elif k == 'name_wrap':
                obj[k] = bool(v) if v is not None and not (isinstance(v, float) and math.isnan(v)) else False
            else:
                obj[k] = clean(v)
        stations[str(obj['id'])] = obj

    # Build station_lines
    station_lines = {}
    for _, row in sl_df.iterrows():
        sl_id = int(row['id'])
        entry = {
            'id': sl_id,
            'station_id': int(row['station_id']),
            'line_id': int(row['line_id']),
            'station_code': str(row['station_code']),
            'join': None,
            'connections': conn_lookup.get(sl_id, [])
        }
        if sl_id in joins_lookup:
            entry['join'] = joins_lookup[sl_id]
        station_lines[str(sl_id)] = entry

    result = {'lines': lines, 'stations': stations, 'station_lines': station_lines}

    if output_path is None:
        output_path = os.path.splitext(input_path)[0]

    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2)
    
    with open("flat_" + output_path, 'w') as f:
        json.dump(result,f)

    print(f"Written to {output_path}")
    print(f"  {len(lines)} lines, {len(stations)} stations, {len(station_lines)} station_lines")


input_path = "singapore_stations.xlsx"
output_path = "out.json"
convert(input_path, output_path)