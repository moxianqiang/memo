from flask import Blueprint, jsonify, g, request
from models import ArticleModel
from exts import db
import datetime

bp = Blueprint("article_bp", __name__)


@bp.route('/article/list', methods=['POST'])
def article_list():
    user = g.user

    if not user:
        return

    articles = ArticleModel.query.filter_by(user_id=user.id).all()

    temp_articles_list = []
    for a in articles:
        temp_articles_list.append({
            'id': a.id,
            'title': a.title,
            'content': a.content,
            'create_time': a.create_time,
            'user_id': a.user_id,
        })

    return jsonify({
        'data': temp_articles_list
    }), 200


@bp.route('/article/add', methods=['POST'])
def article_add():
    user = g.user

    if not user:
        return

    _data = request.get_json()
    title = _data.get('title')
    content = _data.get('content')

    article = ArticleModel(content=content, user_id=user.id, title=title)

    try:
        db.session.add(article)
        db.session.commit()

    except Exception as e:
        # 回滚（只有当所有读写都正确完成时，才不会报错）
        db.session.rollback()
        db.session.flush()
        print('错误：', e)

    return jsonify({
        'msg': '新增笔记成功'
    }), 200


@bp.route('/article/delete', methods=['POST'])
def article_delete():
    # 拿到删除的todo_id
    user = g.user

    if not user:
        return

    _data = request.get_json()
    _id = _data.get('id')

    # 在表删除这条
    article = ArticleModel.query.get(_id)

    try:
        db.session.delete(article)
        db.session.commit()

    except Exception as e:
        # 回滚（只有当所有读写都正确完成时，才不会报错）
        db.session.rollback()
        db.session.flush()
        print('错误：', e)

    return jsonify({
        'msg': '删除笔记成功'
    }), 200


@bp.route('/article/update', methods=['POST'])
def todo_update():
    user = g.user

    if not user:
        return

    _data = request.get_json()
    _id = _data.get('id')
    _title = _data.get('title')
    _content = _data.get('content')

    todo = ArticleModel.query.get(_id)
    todo.title = _title
    todo.content = _content
    todo.create_time = datetime.datetime.now()

    try:
        db.session.commit()

    except Exception as e:
        # 回滚（只有当所有读写都正确完成时，才不会报错）
        db.session.rollback()
        db.session.flush()
        print('错误：', e)

    return jsonify({
        'msg': '修改笔记成功'
    }), 200
