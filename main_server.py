#!/usr/bin/env python3
import argparse

import random
import time
import pandas as pd
import socket
import pickle
from datetime import datetime, timedelta
import paramiko
import os


def ddos_experiment(k, attack_ratio, duration, memo):
    time.sleep(10)
    victim_ip = '10.0.0.100'
    node_number = 50
    sleep_time = 0.07
    start_min = 10  # Attack start minute
    end_min = start_min + duration  # Attack end minute
    active_time = 5  # This is the time step
    attack_start = 0  # It should always be 0 to record the exact attack start time
    duration_delta = timedelta(seconds=duration * 60)
    ip_list = []
    for n in range(1, node_number + 2):
        host_ip = '10.0.0.{}'.format(n)
        ip_list.append(host_ip)
    for ip in ip_list:
        if ip == victim_ip:
            continue
        # ip, active_time, sleep, k, is_ddos, is_end, victim_ip, clk
        active_control_client(ip, active_time, sleep_time, k, False, False, victim_ip, 0, node_number, attack_ratio,
                              attack_start, duration_delta)
    print('Start Tracking')
    treads_dic = dict()

    print('Start Experiment')

    # active_time, start_min, end_min, prec, k, sleep, victim_ip
    node_time_control(active_time, start_min, end_min, attack_ratio, k, sleep_time, victim_ip, node_number,
                      attack_start, duration_delta)

    for key in treads_dic:
        treads_dic[key].join()

    current_time = datetime.now()
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S.%f')
    print('Ending Time', formatted_time)
    print('Experiments End')
    time.sleep(200)
    final_data_processing(victim_ip, ip_list, k, attack_ratio, active_time, duration, memo)
    print('Data Integration Ends')
    # time.sleep(20)


def node_time_control(active_time, start_min, end_min, prec, k, sleep, victim_ip, node_number, attack_start, duration):
    act_dic = dict()
    file_path = './dataFile/NODE_{}.csv'
    df = pd.read_csv('./dataFile/benign_data_2021-01-02 00_00_00_2021-02-01 23_59_58_time_step_600_num_ids_50.csv')
    file_list = df['NODE'].unique().tolist()
    # print(nodes)
    # file_list = ['1152', '13101', '23093', '25668', '27068', '27638', '28381', '31867', '31973', '33925']
    file_path_list = []
    start_min = start_min * 60 / active_time
    end_min = end_min * 60 / active_time
    for path in file_list:
        file_path_list.append(file_path.format(path))
    ip_list = []
    for n in range(1, node_number + 1):
        host_ip = '10.0.0.{}'.format(n)
        ip_list.append(host_ip)
    nums = random.sample(range(len(ip_list)), int(prec * len(ip_list)))
    selected_nodes = []
    for i in nums:
        if ip_list[i] != victim_ip:
            selected_nodes.append(ip_list[i])
    print('Selected Botnet: ', selected_nodes)
    i = 0
    for node in ip_list:
        data_frame = pd.read_csv(file_path_list[i])
        act_list = data_frame['ACTIVE'].to_list()
        act_dic[node] = act_list
        i += 1
    # print(act_dic)
    start_time = time.time()
    clk = 0
    while True:
        if clk > 428:
            break
        clk += 1
        if start_min <= clk < end_min:
            print('attack start')
            if attack_start == 0:
                attack_start = datetime.now()
            ddos_attack_control(ip_list, prec, active_time, sleep, k, victim_ip, clk, node_number, act_dic,
                                selected_nodes, attack_start, duration)
        else:
            for node in ip_list:
                if act_dic[node][clk] == 1:
                    active_control_client(node, active_time, sleep, 0, False, False, victim_ip, clk, node_number, prec,
                                          attack_start, duration)
                    # node.cmd('sudo ./benign_behavior.py --time {} --n 10 --sleep 0.1 &'.format(time_interval))
                    print(node, ' is active.')
            print(clk)
        print('----------------------------')
        time.sleep(active_time)
    for node in ip_list:
        print('Sending End Signal to {}'.format(node))
        active_control_client(node, active_time, sleep, 0, False, True, victim_ip, clk, node_number, prec,
                              attack_start, duration)
        # time.sleep(3)


def active_control_client(ip, active_time, sleep, k, is_ddos, is_end, victim_ip, clk, node_number, attack_ratio,
                          attack_start, duration):
    c_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # arr = [active_time, sleep, k, is_ddos, is_end]
    data_dic = {'active_time': active_time,
                'sleep': sleep,
                'k': k,
                'is_ddos': is_ddos,
                'is_end': is_end,
                'victim_ip': victim_ip,
                'clk': clk,
                'node_ip': ip,
                'node_number': node_number,
                'attack_ratio': attack_ratio,
                'attack_start': attack_start,
                'duration': duration
                }
    c_socket.sendto(pickle.dumps(data_dic), (ip, 9565))


def ddos_attack_control(ip_list, perc, active_time, sleep, k, victim_ip, clk, node_number, act_dic, selected_nodes,
                        attack_start, duration):
    for node in selected_nodes:
        if node != victim_ip:
            active_control_client(node, active_time, sleep, k, True, False, victim_ip, clk, node_number, perc,
                                  attack_start, duration)
    for node in ip_list:
        if node not in selected_nodes and act_dic[node][clk] == 1:
            print(node, ' is active.')
            active_control_client(node, active_time, sleep, 0, False, False, victim_ip, clk, node_number, perc,
                                  attack_start, duration)
    # if '192.168.1.158' in selected_nodes:
    #     print('start attack')
    #     t = threading.Thread(target=ddos_attack_simulation.ddos_attack, args=(victim_ip, active_time, k))
    #     t.start()


def file_transferring_and_generating(host, port, username, password, remote_file_path, local_file_path):
    transport = paramiko.Transport((host, port))
    transport.connect(username=username, password=password)

    sftp = paramiko.SFTPClient.from_transport(transport)
    sftp.get(remote_file_path, local_file_path)

    sftp.close()
    transport.close()


def final_data_processing(victim_ip, ip_list, k, ratio, active_time, duration, memo):
    local_file_path = './dataFile/packet_volume/packet_volume_info_{}.csv'
    final_data = pd.DataFrame()
    for host in ip_list:
        if host == victim_ip:
            continue
        file_path = local_file_path.format(host[7:])
        if not os.path.exists(file_path):
            print('File does not exist:', file_path)
            continue
        print('Processing data from', host)
        df = pd.read_csv(file_path)
        final_data = pd.concat([final_data, df], ignore_index=True)
    final_data.to_csv('./dataFile/final_data/{}_{}_{}_{}_data.csv'.format(k, ratio, duration, memo),
                      index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--k", type=int, default=1)
    parser.add_argument("--ratio", type=float, default=1)
    parser.add_argument("--duration", type=float, default=10)
    parser.add_argument("--memo", type=str, default='training')
    args = parser.parse_args()
    ddos_experiment(args.k, args.ratio, args.duration, args.memo)
