from exts import db
from datetime import datetime

# Integer：整型
# primary_key：作为主键（唯一）
# autoincrement：自增长
# unique：唯一
# default：默认值

# 用户表
class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    gender = db.Column(db.String(10), nullable=False)
    token = db.Column(db.String(300), nullable=False, unique=True)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)

    # 找到用户时，通过 用户.todos拿到该用户下的所有todo
    # 在TodoModel表，也可以找到某条todo，通过todo.user拿到该todo所属的用户
    todos = db.relationship('TodoModel', backref='user', lazy='dynamic')
    articles = db.relationship('ArticleModel', backref='user', lazy='dynamic')


# todo任务表
class TodoModel(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(100), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    is_done = db.Column(db.Boolean, nullable=False, default=False)

    # 外键写在多的一端（一个用户可以有多个todo任务）
    # db.ForeignKey(value)
    # value: 1、'表名.id' 字符串； 2、模型类名.id
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # def __repr__(self):
    #     # print(self.content)
    #     return {
    #         'id': self.id,
    #         'content': self.content,
    #         'create_time': self.create_time,
    #         'is_done': self.is_done,
    #     }


class ArticleModel(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
