import torch
from transformers import AutoModelForCausalLM, BitsAndBytesConfig, AutoTokenizer
import json
import torch
from transformers import LlamaForCausalLM, LlamaTokenizer
from peft import PeftModel, PeftConfig
from torch.cuda.amp import autocast
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
with open('pred.json', 'w', encoding='utf-8') as f:
    json.dump(responses, f)
