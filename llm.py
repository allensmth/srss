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
    
    return content

# test
cc = '''---------- Forwarded message ---------
发件人： YouTube <noreply@youtube.com>
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
ASML 目前的价位680附近可能会考虑开一个观察仓位 不超过0.5%
CVS 56附近之前提到的没开仓的新人考虑 朋友注意一下仓位控制 上限3%左右（具体看真爱粉视频）
谷歌如果仓位大你180附近止盈部分也正常 但是小仓位的话目前继续持有问题不大

具体提问和股票分析请去10.26.2024 Pro贴留言
稍后会聊一下微软 星巴克 Meta等公司财报

本帖仅供参考
未经允许禁止转载
北美王哥财经 LA Banker
<https://www.youtube.com/attribution_link?a=Zd4hVQp5bu_pLjxR&u=/channel/UCW1cHQAzfL3pwKlKNwRjelQ%3Ffeature%3Dem-sponsor>
View post
<https://www.youtube.com/attribution_link?a=Zd4hVQp5bu_pLjxR&u=/channel/UCW1cHQAzfL3pwKlKNwRjelQ/community%3Ffeature%3Dem-sponsor%26lb%3DUgkxxWhZsFtlZ2gyyG1cn5JlGq6JgKiXpZHL>
------------------------------
If you no longer wish to receive emails about members-only posts, you can
unsubscribe
<https://www.youtube.com/attribution_link?noapp=1&a=Zd4hVQp5bu_pLjxR&u=/email_unsubscribe%3Fuid%3DASnvXvtL1mhr-Vn4LIdgxnSy-zHTgaA81uKpJenjCVEiUCv-zFzucnwKb98m%26action_unsubscribe%3Dmembers_only_posts%26timestamp%3D1730321071%26feature%3Dem-sponsor>.
'''
print(extract_text(cc))