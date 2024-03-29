# 使用LoRa在Text-to-SQL任务上微调CodeLlama 7B模型（https://github.com/Mucalinda2436/Codellama_for_SQL.git）

## 步骤说明
### step1. 使用'fine-tuning codellama.py'文件微调7b的codellama。
### step2. 使用'output_results.py'文件生成结果。
### step3. 切换到Evaluation工作目录下，添加Spider数据库的内容到/Evaluation/database/路径下，然后在终端使用代码：python3 evaluation.py --gold ./dev_gold.sql --pred ./pred.sql --etype all --db ./database --table ./tables.json --progress_bar_for_each_datapoint获取评估结果。

## 微调结果
### 第一组参数：r=16, learning rate=2e-4, batch size=28, max_steps=400（蓝色线）
### 第二组参数：r=16, learning rate=2e-5, batch size=28, max_steps=200（红色线）
### 第三组参数：r=16, learning rate=2e-6, batch size=28, max_steps=200（绿色线）
### 训练情况：
![image text](https://github.com/Mucalinda2436/Codellama_for_SQL/blob/main/img_folder/%E6%88%AA%E5%B1%8F2024-01-15%2016.10.53.png)
![image text](https://github.com/Mucalinda2436/Codellama_for_SQL/blob/main/img_folder/%E6%88%AA%E5%B1%8F2024-01-15%2016.10.44.png)

## 分析
### 训练指标分析：

#### 训练步骤每秒（train_steps_per_second）:

第三组的训练拥有最高的步骤速度，意味着该模型每秒可以执行更多的训练步骤。
第一组的训练步骤速度最慢。

#### 样本每秒（train_samples_per_second）:

与训练步骤每秒类似，第三组的训练也在样本处理速度上领先。
第一组在这个指标上表现最差。

#### 损失率（train_loss）:

第三组的训练损失最低，这通常意味着模型的性能有所提升。
相比之下，第一组的损失率最高，可能表明模型的拟合效果不佳或者学习过程有困难。

#### 学习率（learning_rate）:

第三组的训练中，学习率呈现出先增后减的趋势，这可能是采用了某种自适应学习率调整策略，如学习率预热或退火策略。
第一组和第二组的学习率保持较为平稳，但第二组的学习率普遍高于第一组。

#### 周期（epoch）:

第三组的训练周期数最多，说明在给定时间内进行了更多的完整数据集迭代。
第一组的训练周期数最少。

### 评估指标分析：

#### 评估步骤每秒（steps_per_second）:

与训练过程类似，第三组的评估也是最快的。
第一组的评估步骤速度最慢。

#### 运行时间（runtime）:

第三组的评估运行时间随着步骤的增加而缓慢增长，这表明其性能较为稳定。
第一组和第二组的运行时间则有较大波动，可能表明评估过程中有性能瓶颈。

#### 损失率（loss）:

第三组的评估损失逐步下降，稳定在较低的水平，这指示出模型在评估集上的表现良好且稳定。
第一组开始时损失较高，但迅速下降，这可能是因为模型在学习初期调整了参数，快速改进了性能。
第二组的损失率起初降低，随后平稳，但整体上损失较2024-01-14要高。

#### 样本每秒（samples_per_second）:

第三组在样本处理速度上同样表现最佳，这表明它在处理评估数据时更加高效。
第一组的样本处理速度最慢，这可能影响到模型评估的整体效率。

## Spider测试数据上的效果
![image text](https://github.com/Mucalinda2436/Codellama_for_SQL/blob/main/img_folder/%E8%AE%AD%E7%BB%83%E7%9A%84codellama1-100%EF%BC%88%E6%9C%80%E5%A5%BD%E7%9A%84%E7%BB%93%E6%9E%9C%EF%BC%89.png)
在Spider测试数据上，第二组得到了最好的结果，有44%左右的正确率，而第一组只有30%，第三组38%。这也许是因为第一组的模型过拟合较为严重，而第三组的训练效果不如第二组。
