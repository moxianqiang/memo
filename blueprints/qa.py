from flask import Blueprint, session, get_flashed_messages, jsonify, make_response

bp = Blueprint("qa_bp", __name__)


@bp.route('/list')
def index():
    print('访问 /api/list', session['session_id'])
    _f = get_flashed_messages(category_filter=['flash_message'])

    if len(_f) > 0:
        print('闪现值：', _f)
    else:
        print('没有闪现值')

    response = make_response(jsonify({
        'status': 'OK',
        'message': '列表页面'
    }))

    return response, 200, {'Content-Type': 'application/json; charset=UTF-8'}
