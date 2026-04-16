import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

code = ""
# 读取code.py文件并把内容存到code变量中
current_dir = os.path.dirname(os.path.abspath(__file__))
code_path = os.path.join(current_dir, 'code.py')
with open(code_path, 'r', encoding='utf-8') as file:
    code = file.read()

client = OpenAI(
    api_key=os.getenv('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com/v1")

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是一位出色的工程师，请根据用户的提问，回答用户的问题。"},
        {"role": "user", "content": f"请分析这段代码：{code}"},
    ],
    stream=False
)

print(response.choices[0].message.content)