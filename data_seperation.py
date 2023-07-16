import pandas as pd

# 读取CSV文件
df = pd.read_csv('C:/Users/jiahe/Downloads/benign_data_2021-01-02 00_00_00_2021-02-01 23_59_58_time_step_600_num_ids_50.csv')

# 根据"NODE"列的值进行分组
grouped = df.groupby('NODE')

# 遍历每个分组
for node, group in grouped:
    # 创建以节点名命名的新文件
    filename = f'C:/Application Profile/Python/pythonProject3/NODE_{node}.csv'
    # 保存当前分组的数据到新文件
    group.to_csv(filename, index=False)
