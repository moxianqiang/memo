from flask import Blueprint, redirect, session, flash, jsonify, make_response, url_for
# from .decorators.auth import login_auth

bp = Blueprint("login_bp", __name__)


@bp.route('/login', methods=['GET', 'POST'])
# @login_auth
def login():
    print('post登录接口')
    session['session_id'] = 'abc666'
    flash('用户已经登录', category='flash_message')

    response = make_response(jsonify({
        'status': 'OK',
        'message': '登录页面'
    }))
    response.headers.add('Content-Type', 'application/json; charset=utf-8')

    return response

    # email = request.form.email
    # password = request.form.password

    # 校验email格式
    # 通过邮箱在用户表中找到用户，比对密码是否正确
    # 如果正确，跳转到首页；如果不正确，跳转到登录页

    # bol = True
    #
    # if bol:
    #     session['session_id'] = 'email'
    #     return '首页'
    # else:
    #     return '登录页面'


@bp.route('/logout', methods=['POST'])
def logout():
    # 1，删除session的cookie
    # session.pop('xxx', None)
    # 或 session.clear()

    # 2，返回到登录页面
    return redirect(url_for('login'))
