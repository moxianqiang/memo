from flask import Blueprint, abort

bp = Blueprint("error_bp", __name__)


@bp.route('/error')
def index():
    abort(404)
