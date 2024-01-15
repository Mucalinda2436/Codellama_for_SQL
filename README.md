# 使用LoRa在Text-to-SQL任务上微调CodeLlama 7B模型

## 步骤说明
### step1. 使用'fine-tuning codellama.py'文件微调7b的codellama。
### step2. 使用'output_results.py'文件生成结果。
### step3. 切换到Evaluation工作目录下，添加Spider数据库的内容到/Evaluation/database/路径下，然后在终端使用代码：python3 evaluation.py --gold ./dev_gold.sql --pred ./pred.sql --etype all --db ./database --table ./tables.json --progress_bar_for_each_datapoint获取评估结果。

## 微调结果
### 第一组参数：r=16, learning rate=2e-4, batch size=28, max_steps=400（蓝色线）
### 第二组参数：r=16, learning rate=2e-5, batch size=28, max_steps=200（红色线）
### 第三组参数：r=16, learning rate=2e-6, batch size=28, max_steps=200（绿色线）
### 训练情况：
![image text](https://github.com/Mucalinda2436/Codellama_for_SQL/blob/main/img_folder/%E6%88%AA%E5%B1%8F2024-01-15%2016.10.44.png)
