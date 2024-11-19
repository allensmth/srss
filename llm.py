#llm.py

import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

llm_client = Groq(
    api_key= os.getenv('LLM_KEY')
)

PROMPT = '''这个是个mail的内容文本,提取这个文本里面的文字内容,去掉收件人发件人信息,去掉各种image和url以及youtube链接,去掉和unsubscribe相关的文字说明内容,把文本返回到json格式内,文本如下:"'''

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
    # 截取 content 中的 JSON 字符串
    json_str = content[content.find("{"):content.rfind("}")+1]
    # 解析 JSON 字符串
    json_data = json.loads(json_str)
    # 提取 text 字段
    text = json_data.get("text", "")
    # 将换行符替换为 <br/>
    text = text.replace("\n", "<br/>")
    
    return text

# test
cc = '''---------- Forwarded message ---------
��件人： YouTube <noreply@youtube.com>
Date: 2024年10月31日周四 04:44
Subject: For members only: new 北美王哥财经 LA Banker post
To: james yng <ljatreeyang@gmail.com>


[image: Youtube Logo]
<https://www.youtube.com/attribution_link?a=Zd4hVQp5bu_pLjxR&u=/>
Members only
<https://www.youtube.com/attribution_link?a=Zd4hVQp5bu_pLjxR&u=/channel/UCW1cHQAzfL3pwKlKNwRjelQ%3Ffeature%3Dem-sponsor>
真爱粉贴 10.30.2024

按照之前的计划NKE在76.50~78之间完成了1%加仓
PFE目前的价位28附近没开仓的新人 自己可以考虑一下1-2%仓位
'''

cleaned_text = extract_text(cc)
print(cleaned_text)