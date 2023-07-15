#!/usr/bin/env python3
import csv
import os

data_info = ['BEGIN_DATE',
                 'END_DATE',
                 'NUM_NODES',
                 'ATTACK_RATIO',
                 'ATTACK_START_TIME',
                 'ATTACK_DURATION',
                 'ATTACK_PARAMETER',
                 'NODE',
                 'LAT',
                 'LNG',
                 'TIME',
                 'TIME_FEATURE',
                 'ACTIVE',
                 'PACKET',
                 'ATTACKED']

file_path = '/home/ee597/Desktop/MiniTest/dataFile/packet_volume/packet_volume_info_{}.csv'.format('10.0.0.2')[-1:]

try:
    with open(file_path, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=data_info)
        writer.writeheader()
except FileExistsError:
    pass
# # Try to read the file to check its content
# with open(file_path, 'r') as file:
#     reader = csv.reader(file)
#     print("File content:")
#     for row in reader:
#         print(row)
