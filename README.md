
## 微信机器人微调模型实践指南

<br>

### 第一步：选择合适的大型语言模型

当前可选择的开源的大型语言模型有很多，不同的参数规格。考虑到廉颇老矣，且只有11G显存，参数量不可能太多。我分别测试了三个大型语言模型 Llama3-Chinese-8B-Instruct（基于Llama3的中文微调模型）、ChatGLM3-6b （智谱AI和清华大学联合开发）、Atom-7B-Chat（基于Llama2且采用中文语料进行预训练），从响应速度，回复质量，中文支持表现多方面考察后选择了Atom-7B-Chat模型。（模型可在魔搭社区下载）

在运行模型前，需要安装CUDA和对应版本的Torch，其他模块按照对应开源模型的```requirement.txt```进行安装即可。模型下载完成后，根据提供的快速运行例程代码，修改好模型所在的目录，调整参数，终端Python即可运行模型。（注：此时你已经有了一个通用的语言大模型了）

由于1080Ti显卡架构比较老，初始化模型中遇到了各种问题（比如不支持flash_attention以及显存不足），但在网上大多有解决方案。

<br>

### 第二步：提取微信聊天记录

要想训练基于自己语言风格的模型，先要有高质量/大数量的对话数据，就涉及到数据的提取和预处理。微信电脑端的数据是加密保存在本地的，使用了Github上的开源项目“留痕”进行导出。

项目链接： https://github.com/LC044/WeChatMsg

按照使用说明，将手机端的聊天数据迁移到电脑端，重启电脑端微信后解析数据，点击对应的好友，即可导出聊天数据。软件可以选择导出的数据格式有很多，由于不同的语言模型训练数据要求的格式可能不同，为了匹配我使用的Atom-7B-Chat模型，导出了TXT数据格式。

随后对TXT聊天数据进行预处理，数据清洗。每个人的聊天风格不太一样，比如可能对方发了很多消息，随后我依次回复，这时数据比较杂乱，可能不利于模型的学习，因此我只提取了引用部分的对话（因为这部分对话具有很强的因果关系，有利于模型的模式识别）。但是因此数据量也急剧地减小，大概1000次对话。

对于准备好的数据，需要将它们转换为模型训练要求的格式，Atom-7B-Chat以及对应的Lora微调要求类似 ```<s>Human: 女孩子生气的时候是不是暂时不能讲理啊</s><s>Assistant: 嗯嗯</s>``` 的csv格式，因此还需要进行格式转换，以及训练集与验证集的分配。（利用gpt可轻松完成代码编写）

<br>

### 第三步：Lora微调训练

由于显卡性能限制，选择Lora微调。

项目链接：https://github.com/LlamaFamily/Llama-Chinese 

步骤二中的训练集和验证集需要放入data文件夹中，进入train/sft 选择finetune_lora.sh 进行微调训练，需要先修改```finetune_clm_lora.py``` 以及 ```finetune_lora.sh``` 里的参数，指定原模型和微调后模型的文件位置，根据需要修改``` epoch，Batch size，lora_alpha ```等参数。

<br>

### 第四步：封装模型，创建兼容OpenAI的API接口（参见github项目 Llama-Chinese\train\sft\server.py）

对微调模型进行测试，随后进行按照openai的请求和响应格式进行Flask封装，对外提供API服务。

<br>

### 第五步：接入微信聊天机器人

项目链接：https://github.com/zhayujie/chatgpt-on-wechat

修改config.json文件（修改```bot_type:chatGPT```，修改```open_ai_api_base```为模型运行地址，以此兼容支持openai请求格式的第三方大模型），随后扫码登录。可在windows上运行，也可以部署在服务器上。

<br>

### 效果图

![alt 效果图](https://github.com/Lucky-183/wechat_bot_practice/blob/master/result.jpg)

<br>

### 参考&感谢

https://github.com/LC044/WeChatMsg 提取微信聊天记录，将其导出成HTML、Word、Excel文档永久保存。

https://github.com/li-plus/chat4u 用微信聊天记录训练一个你专属的聊天机器人。

https://github.com/xming521/WeClone 使用微信聊天记录微调大语言模型，并绑定到微信机器人，实现自己的数字克隆。

https://github.com/zhayujie/chatgpt-on-wechat 基于大模型搭建的聊天机器人，同时支持 微信公众号、企业微信应用、飞书、钉钉 等接入。

https://github.com/LlamaFamily/Llama-Chinese Llama中文社区
