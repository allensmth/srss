from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from datetime import datetime
from dotenv import load_dotenv
import os

# 加载环境变量
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
    rss_items = RSS.query.all()
    return render_template('index.html', rss_items=rss_items)

@app.route('/add_rss', methods=['POST'])
def add_rss():
    data = request.get_json()
    content = data.get('content')
    author = data.get('author')
    label = data.get('label')
    created_at = data.get('created_at', datetime.utcnow())

    if not content or not author:
        return jsonify({'error': 'Content and author are required'}), 400

    new_rss = RSS(content=content, author=author, label=label, created_at=created_at)
    db.session.add(new_rss)
    db.session.commit()

    # 通过 WebSocket 通知客户端
    socketio.emit('new_rss', {
        'id': new_rss.id,
        'content': new_rss.content,
        'author': new_rss.author,
        'label': new_rss.label,
        'created_at': new_rss.created_at.strftime('%Y-%m-%d %H:%M:%S')
    })

    return jsonify({'message': 'RSS item added successfully'}), 201

@app.route('/search_rss', methods=['GET'])
def search_rss():
    label = request.args.get('label')
    if not label:
        return jsonify({'error': 'Label is required'}), 400

    rss_items = RSS.query.filter_by(label=label).all()
    return jsonify([{
        'id': item.id,
        'content': item.content,
        'author': item.author,
        'label': item.label,
        'created_at': item.created_at.strftime('%Y-%m-%d %H:%M:%S')
    } for item in rss_items])

if __name__ == "__main__":
    socketio.run(app, debug=True)