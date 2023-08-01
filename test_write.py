#!/usr/bin/env python3
import pandas as pd

# 读取CSV文件
df = pd.read_csv('./dataFile/benign_data_2021-01-02 00_00_00_2021-02-01 23_59_58_time_step_600_num_ids_50.csv')

# 提取"NODE"列的唯一值
nodes = df['NODE'].unique().tolist()

# 打印结果
print(nodes)
