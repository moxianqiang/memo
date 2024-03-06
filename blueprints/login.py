from flask import Blueprint, flash, jsonify, request, g
# from .decorators.auth import login_auth
from models import UserModel
from exts import db
import random
import uuid

bp = Blueprint("login_bp", __name__)


@bp.route('/login', methods=['POST'])
# @login_auth
def login():
    _data = request.get_json()

    email = _data.get('email')
    password = _data.get('password')

    user = UserModel.query.filter_by(email=email).first()

    if user:
        if user.password == password:
            flash('用户登录成功', category='flash_message')

            return jsonify({
                'msg': '登录成功！',
                'token': user.token
            }), 200

        else:
            return jsonify({
                'msg': '密码错误！',
            }), 403
    else:
        return jsonify({
            'msg': '该邮箱还未注册！',
        }), 403

    # response = make_response()
    # response.headers.add('Content-Type', 'application/json; charset=utf-8')
    # return response


@bp.route('/logout', methods=['POST'])
def logout():
    # 1，删除session的cookie
    # session.pop('session_id', None)  # 删除某个
    # session.clear()  # 删除所有（慎用）

    # 2，返回
    # return redirect(url_for('login'))  # 跳转登录页面视图
    # 返回退出成功的数据
    return jsonify({
        'msg': '退出成功！',
    }), 200


@bp.route('/register', methods=['POST'])
def register():
    _data = request.get_json()

    email = _data.get('email')
    password = _data.get('password')
    password2 = _data.get('password2')

    if password != password2:
        return jsonify({
            'msg': '两次密码不一致！',
        }), 403

    user = UserModel.query.filter_by(email=email).first()

    if user:
        return jsonify({
            'msg': '账号注册失败！该邮箱已存在用户',
        }), 403
    else:
        username = '游客 %s' % random.randint(10000000, 99999999)
        token = str(uuid.uuid4())

        _user = UserModel(
            email=email,
            password=password,
            gender='男',
            username=username,
            token=token
        )

        db.session.add(_user)
        db.session.commit()

        return jsonify({
            'msg': '账号注册成功',
        }), 200

