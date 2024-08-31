import random
import csv

# 读取 output.txt 的内容
with open('output.txt', 'r', encoding='utf-8') as file:
    output_lines = file.readlines()

# 读取 output_from_quotes.txt 的内容
with open('output_from_quotes.txt', 'r', encoding='utf-8') as file:
    output_from_quotes_lines = file.readlines()

# 将两者内容合并
combined_lines = output_from_quotes_lines + output_lines

# 随机打乱顺序
# random.shuffle(combined_lines)

# 计算训练集和验证集的切分索引
split_index = int(len(combined_lines) * 0.9)

# 切分训练集和验证集
train_lines = combined_lines[:]
val_lines = combined_lines[split_index:]

# 将训练集内容写入 train.csv
with open('train.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['text'])  # 添加列名
    for line in train_lines:
        writer.writerow([line.strip()])  # 每一行作为一个单独的列数据

# 将验证集内容写入 val.csv
with open('val.csv', 'w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['text'])  # 添加列名
    for line in val_lines:
        writer.writerow([line.strip()])  # 每一行作为一个单独的列数据

print("Splitting complete. Check 'train.csv' and 'val.csv' for the results.")
