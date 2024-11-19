from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from datetime import datetime
from pytz import timezone
from dotenv import load_dotenv
import os
 #这里是引入llm.py中的extract_text函数
from llm import extract_text


load_dotenv()

app = Flask(__name__)
app.config.from_object('config.Config')
db = SQLAlchemy(app)
socketio = SocketIO(app, async_mode='eventlet')

class RSS(db.Model):
    __tablename__ = 'rss'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    label = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)

@app.route('/')
def index():
    rss_items = RSS.query.order_by(RSS.created_at.desc()).all()
    authors = db.session.query(RSS.author).distinct().all()
    authors = [author[0] for author in authors]  # 提取作者名

    # 将时间转换为北京时间
    beijing_tz = timezone('Asia/Shanghai')
    for item in rss_items:
        item.created_at = item.created_at.astimezone(beijing_tz)

    return render_template('index.html', rss_items=rss_items, authors=authors)

def save_rss(content, author, label, created_at):
    if not content or not author:
        return {'error': 'Content and author are required'}, 400

    new_rss = RSS(content=content, author=author, label=label, created_at=created_at)
    db.session.add(new_rss)
    db.session.commit()

    # 将时间转换为北京时间
    beijing_tz = timezone('Asia/Shanghai')
    created_at_beijing = new_rss.created_at.astimezone(beijing_tz)

    socketio.emit('new_rss', {
        'id': new_rss.id,
        'content': new_rss.content,
        'author': new_rss.author,
        'label': new_rss.label,
        'created_at': created_at_beijing.strftime('%Y-%m-%d %H:%M:%S')
    })

    return {'message': 'RSS item added successfully'}, 201


@app.route('/add_rss_form', methods=['POST'])
def add_rss_form():
    content = request.form.get('content')
    author = request.form.get('author')
    label = request.form.get('label')
    created_at = datetime.utcnow()
    content = extract_text(content)
    print("content:" + content)
    if not content:
        content="empty"
    response, status = save_rss(content, author, label, created_at)
    return jsonify(response), status

@app.route('/add_rss', methods=['POST'])
def add_rss():
    data = request.get_json()
    content = data.get('content')
    author = data.get('author')
    label = data.get('label')
    created_at = data.get('created_at', datetime.utcnow())

    response, status = save_rss(content, author, label, created_at)
    return jsonify(response), status

@app.route('/filter', methods=['POST'])
def search_rss():
    author = request.form.get('author')
    label = request.form.get('label')
    print(f"Author: {author}, Label: {label}")
    query = RSS.query
    
    if author and author != 'all':
        query = query.filter_by(author=author)
    
    if label:
        query = query.filter_by(label=label)
    
    rss_items = query.order_by(RSS.created_at.desc()).all()

    # 将时间转换为北京时间
    beijing_tz = timezone('Asia/Shanghai')
    for item in rss_items:
        item.created_at = item.created_at.astimezone(beijing_tz)
    
    return render_template('post_list.html', rss_items=rss_items)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=8080 , debug=True)