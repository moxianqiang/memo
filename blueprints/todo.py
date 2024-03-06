import datetime
from flask import Blueprint, request, jsonify, g
from exts import db
from models import TodoModel

bp = Blueprint("todo_bp", __name__)


@bp.route('/todo/list', methods=['POST'])
def todo_list():
    user = g.user

    if not user:
        return

    todos = TodoModel.query.filter_by(user_id=user.id).all()
    print('todos：', todos)

    temp_todo_list = []
    for t in todos:
        temp_todo_list.append({
            'id': t.id,
            'content': t.content,
            'create_time': t.create_time,
            'is_done': t.is_done,
            'user_id': t.user_id,
        })

    return jsonify({
        'data': temp_todo_list
    }), 200


@bp.route('/todo/add', methods=['POST'])
def todo_add():
    user = g.user

    if not user:
        return

    _data = request.get_json()
    content = _data.get('content')

    todo = TodoModel(content=content, user_id=user.id)

    try:
        db.session.add(todo)
        db.session.commit()

    except Exception as e:
        # 回滚（只有当所有读写都正确完成时，才不会报错）
        db.session.rollback()
        db.session.flush()
        print('错误：', e)

    return jsonify({
        'msg': '新增任务成功'
    }), 200


@bp.route('/todo/update', methods=['POST'])
def todo_update():
    user = g.user

    if not user:
        return

    _data = request.get_json()
    _id = _data.get('id')
    _content = _data.get('content')
    _is_done = _data.get('is_done')

    todo = TodoModel.query.get(_id)
    todo.content = _content
    todo.is_done = _is_done
    todo.create_time = datetime.datetime.now()

    try:
        db.session.commit()

    except Exception as e:
        # 回滚（只有当所有读写都正确完成时，才不会报错）
        db.session.rollback()
        db.session.flush()
        print('错误：', e)

    return jsonify({
        'msg': '修改任务成功'
    }), 200


@bp.route('/todo/delete', methods=['POST'])
def todo_delete():
    # 拿到删除的todo_id
    user = g.user

    if not user:
        return

    _data = request.get_json()
    _id = _data.get('id')

    # 在表删除这条
    todo = TodoModel.query.get(_id)

    try:
        db.session.delete(todo)
        db.session.commit()

    except Exception as e:
        # 回滚（只有当所有读写都正确完成时，才不会报错）
        db.session.rollback()
        db.session.flush()
        print('错误：', e)

    return jsonify({
        'msg': '删除任务成功'
    }), 200
