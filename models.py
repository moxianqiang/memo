from exts import db
from datetime import datetime


# 用户表
class UserModel(db.Model):
    __tablename__ = 'user'
    # 主键：整型Integer，作为主键（唯一）primary_key，自增长autoincrement
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    gender = db.Column(db.String(10), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
