import pandas as pd
import json
import math
import sys
import os

def clean(v):
    if isinstance(v, float):
        if math.isnan(v): return None
        if v.is_integer(): return int(v)
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

    # Build connections lookup: cur_station_line -> list
    conn_lookup = {}
    for _, row in connections_df.iterrows():
        sid = int(row['cur_station_line'])
        if sid not in conn_lookup:
            conn_lookup[sid] = []
        conn_lookup[sid].append({
            'cur_station_line': int(row['cur_station_line']),
            'next_station_line': int(row['next_station_line']),
            'line_id': clean(row['line']),
            'connection_style': str(row['connection_style'])
        })

    # Build joins lookup: station_line_id -> list
    joins_lookup = {}
    for _, row in joins_df.iterrows():
        sid = int(row['station_line_id'])
        if sid not in joins_lookup:
            joins_lookup[sid] = []
        joins_lookup[sid].append({
            'join': int(row['join']),
            'position': str(row['position']),
            'offset': int(row['offset']),
            'separate': bool(row['separate'])
        })

    # Build stations
    stations = {}
    for _, row in stations_df.iterrows():
        obj = {k: clean(v) for k, v in row.items()}
        stations[str(obj['id'])] = obj

    # Build station_lines
    station_lines = {}
    for _, row in sl_df.iterrows():
        sl_id = int(row['id'])
        station_lines[str(sl_id)] = {
            'id': sl_id,
            'station_id': int(row['station_id']),
            'line_id': int(row['line_id']),
            'station_code': str(row['station_code']),
            'connections': conn_lookup.get(sl_id, []),
            'joins': joins_lookup.get(sl_id, [])
        }

    result = {'lines': lines, 'stations': stations, 'station_lines': station_lines}

    if output_path is None:
        output_path = os.path.splitext(input_path)[0] + '.json'

    with open(output_path, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"Written to {output_path}")
    print(f"  {len(lines)} lines, {len(stations)} stations, {len(station_lines)} station_lines")


input_path = "singapore_stations.xlsx"
output_path = "out.json"
convert(input_path, output_path)