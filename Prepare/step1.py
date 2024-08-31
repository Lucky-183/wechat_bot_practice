import re

# 读取对话内容
with open('小石_chat.txt', 'r', encoding='utf-8') as file:
    conversation = file.read()

# 定义用户和助手的名字
human = "小石"
assistant = "忘忧"

# 将对话转换为目标格式
output = []
dialogue = []
for line in conversation.splitlines():
    line = line.strip()
    if not line or line.startswith("*"):
        continue
    if line.startswith(f"{human}:"):
        dialogue.append(f"<s>Human: {line[len(human) + 1:].strip()}</s>")
    elif line.startswith(f"{assistant}:"):
        dialogue.append(f"<s>Assistant: {line[len(assistant) + 1:].strip()}</s>")

    if len(dialogue) == 2:
        output.append(f'"{"".join(dialogue)}"')
        dialogue = []

# 将结果写入文件
with open('output.txt', 'w', encoding='utf-8') as file:
    file.write("\n".join(output))

print("Conversion complete. Check 'output.txt' for the result.")
