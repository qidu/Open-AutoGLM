from openai import OpenAI
import requests

client = OpenAI(
    base_url='https://api-inference.modelscope.cn/v1',
    api_key='ms-2e0bb290-a6f8-454a-9c04-d777d7ca8151', # ModelScope Token
)

json_url = "https://modelscope.oss-cn-beijing.aliyuncs.com/phone_agent_test.json"
response_json = requests.get(json_url)
messages = response_json.json()

response = client.chat.completions.create(
    model='ZhipuAI/AutoGLM-Phone-9B', # ModelScope Model-Id, required
    messages=messages,
    temperature=0.0,
    max_tokens=1024,
    stream=False
)

print(response.choices[0].message.content)
