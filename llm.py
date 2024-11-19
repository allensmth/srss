#llm.py

import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

llm_client = Groq(
    api_key= os.getenv('LLM_KEY')
)



PROMPT = '''这个是个mail的内容文本,提取这个文本里面的文字内容,去掉各种image和url等内容:"'''
def extract_text(content):
    chat_completion = llm_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": PROMPT + content + "\"",
            }
        ],
        
        model="mixtral-8x7b-32768",
    )
    content = chat_completion.choices[0].message.content
    #截取content中的json字符串
    content = content[content.find("{"):content.rfind("}")+1]
    return content


