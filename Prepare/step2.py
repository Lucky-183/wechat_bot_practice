import re

# 读取对话内容
with open('小石.txt', 'r', encoding='utf-8') as file:
    conversation = file.read()

# 将对话分行处理
lines = conversation.splitlines()

# 用于存储符合条件的对话
output = []

# 遍历每一行，检查条件并提取对话
for i in range(2, len(lines)):
    current_line = lines[i].strip()
    two_lines_before = lines[i-2].strip()

    # 检查当前行是否以“引用:สาลี่”开头，并且倒数第二行包含“忘忧”
    if current_line.startswith("引用:สาลี่") and "忘忧" in two_lines_before:
        assistant_response = lines[i-1].strip()
        human_text = current_line.split("引用:สาลี่：", 1)[-1].strip()

        if human_text not in ["【表情包】", "【图片消息】", "【视频消息】", "【语音消息】"]:
            output.append(f'"<s>Human: {human_text}</s><s>Assistant: {assistant_response}</s>"')

# 将结果写入文件
with open('output_from_quotes.txt', 'w', encoding='utf-8') as file:
    file.write("\n".join(output))

print("Conversion complete. Check 'output_from_quotes.txt' for the result.")
