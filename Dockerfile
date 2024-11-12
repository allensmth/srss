# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12.7

FROM python:${PYTHON_VERSION}-slim

LABEL fly_launch_runtime="flask"

# 安装 Node.js 和 npm
RUN apt-get update && apt-get install -y nodejs npm && rm -rf /var/lib/apt/lists/*

WORKDIR /code

# 复制并安装 Python 依赖
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# 复制并安装 Node.js 依赖
COPY package.json package-lock.json ./
RUN npm install

# 复制应用代码
COPY . .

# 使用 tailwindcss 生成 CSS
RUN npx tailwindcss -i ./static/src/main.css -o ./static/dist/main.css --minify

# 暴露端口
EXPOSE 8080

# 设置环境变量
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080

# 使用非root用户运行应用
RUN useradd -m flaskuser
USER flaskuser

# 启动命令
CMD ["python3", "-m", "flask", "run", "--host=0.0.0.0", "--port=8080"]