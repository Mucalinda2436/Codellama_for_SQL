import torch
from transformers import AutoModelForCausalLM, BitsAndBytesConfig, AutoTokenizer
import json
import torch
from transformers import LlamaForCausalLM, LlamaTokenizer
from peft import PeftModel, PeftConfig
from torch.cuda.amp import autocast
import re
# 加载原模型
base_model = "codellama/CodeLlama-7b-hf"
model = AutoModelForCausalLM.from_pretrained(
    base_model,
    load_in_8bit=False,
    torch_dtype=torch.float16,
    device_map="auto",
)
tokenizer = AutoTokenizer.from_pretrained("codellama/CodeLlama-7b-hf")
# 加载微调的模型
model = PeftModel.from_pretrained(model, '/data/home/huangziwei/cjk_works/sql-code-llama/checkpoint-400')

with open('question_base.json', 'r') as f:
    data = json.load(f)

responses = []
for i in range(len(data):
    eval_prompt = data[i]['text']
    model_input = tokenizer(eval_prompt, return_tensors="pt").to("cuda")
    model.eval()
    with torch.no_grad(), autocast():
        response = tokenizer.decode(model.generate(**model_input, max_new_tokens=100)[0], skip_special_tokens=True)
        idx = response.find('SELECT')
        response = response[idx: ]
        responses.append(response)
    torch.cuda.empty_cache()
    
# 清洗数据
def clean_sql(sql):
    # 清除换行符和制表符
    sql = sql.replace("\n", " ").replace("\t", " ")

    # 清除多余的空格
    sql = " ".join(sql.split())

    # 如果存在"### Explanation:"，将其之后的文本全部删除
    sql = re.sub(r'###.*', '', sql)

    # 检查是否SQL被分段
    if "SELECT" not in sql:
        # 如果没有SELECT关键字，可能是被分段了，将多行合并成一行
        sql = " ".join(sql.split())

    return sql
    
num = 1
data = data1 + data2 + data3
for i in range(len(responses)):
    sql = responses[i]
    cleaned_sql = clean_sql(sql)
    with open('/Evaluation/pred.sql', 'a') as f:
        # f.writelines(f'###SQL {num}\n')
        f.writelines(cleaned_sql + '\n')
        num += 1
