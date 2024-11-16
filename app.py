from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from datetime import datetime
from dotenv import load_dotenv
import os

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
    authors = db.session.query(RSS.author).distinct().all()
    authors = [author[0] for author in authors]  # 提取作者名
    return render_template('index.html', rss_items=rss_items, authors=authors)

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

    socketio.emit('new_rss', {
        'id': new_rss.id,
        'content': new_rss.content,
        'author': new_rss.author,
        'label': new_rss.label,
        'created_at': new_rss.created_at.strftime('%Y-%m-%d %H:%M:%S')
    })

    return jsonify({'message': 'RSS item added successfully'}), 201

@app.route('/filter', methods=['GET'])
def search_rss():
    author = request.args.get('author')
    if not author:
        return jsonify({'error': 'Label is required'}), 400
    if author == 'all':
        rss_items = RSS.query.all()
    else: 
        rss_items = RSS.query.filter_by(author=author).all()
    
    authors = db.session.query(RSS.author).distinct().all()
    authors = [author[0] for author in authors]  # 提取作者名
    
    return render_template('post_list.html', current_author = author,   rss_items=rss_items, authors=authors)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000 , debug=True)