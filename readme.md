## Flask + Htmlx + daisyUI 程序模板

使用 Flask Htmlx Tailwind CSS 和 daisyUI 搭建一个简单的 web 全栈开发环境。

## 使用步骤

创建虚拟环境

```bash
py -3 -m venv venv
source venv/bin/activate # or
.\venv\Scripts\Activate.ps1
```

安装依赖包

```bash
pip install -r requirements.txt
```

安装 Tailwind CSS 和 daisyUI

```bash
npm install
```

使用 tailwindcss 生成 CSS

```bash
npx tailwindcss -i ./static/src/main.css -o ./static/dist/main.css --minify
```

运行

```bash
(venv)$ python app.py
```

