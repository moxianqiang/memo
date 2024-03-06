from flask import Flask, request, signals, jsonify, current_app, g
from flask.signals import _signals
import config
from flask_cors import CORS
from exts import init_plugins, cache
import time
from models import UserModel

# 导入蓝图
from blueprints.login import bp as login_bp
from blueprints.article import bp as article_bp
from blueprints.todo import bp as todo_bp
from blueprints.error import bp as error_bp


app = Flask(__name__)

# 给app定配置信息
app.config.from_object(config)
# app.config.from_pyfile('config.py')

init_plugins(app=app)

api_prefix = config.url_prefix
# 注册蓝图
app.register_blueprint(login_bp, url_prefix=api_prefix)
app.register_blueprint(article_bp, url_prefix=api_prefix)
app.register_blueprint(todo_bp, url_prefix=api_prefix)
app.register_blueprint(error_bp)

# Flask3.0之后，没有before_first_request
# @app._got_first_request
# def before_first_request_func():
#     # 这里的第一次跟用户和客户端无关，是服务器的第一次
#     print('项目启动初始化一些事情...')


# 请求拦截器（钩子函数 hook）
@app.before_request
def before_request_func():
    if request.method == 'OPTIONS':
        return

    res = jsonify({
        'message': '请求太频繁了',
        'code': 403,
        'status': 'success'
    })

    # 反爬：
    # 1，非浏览器访问
    # 对于来源是python/requests开头，就是python的请求库模拟请求，禁用，防止爬虫
    if 'python' in request.user_agent.string:
        return res

    # 2，同一个ip，频繁访问
    # request.remote_addr：ip地址
    # ip = request.remote_addr
    # if cache.get(ip):
    #     return res
    # else:
    #     cache.set(ip, 'abc', timeout=1)

    # 把用户对象放到g全局对象上
    _data = request.get_json()
    token = _data.get('token', None)
    if token:
        g.user = UserModel.query.filter_by(token=token).first()
    else:
        g.user = None


# 上下文处理器（钩子函数 hook）
@app.context_processor
def context_processor_func():
    pass


@app.errorhandler(404)
def error_func(err):
    return '自定义错误：%s' % err


# def signal_func(*args, **kwargs):
#     # *args, **kwargs 形参必须填上
#     print('request_started信号 -> ', *args, **kwargs)


# 信号（有很多个，类似于vue的生命周期钩子，如果信号有写代码，就执行，没写代码跳过）
# signals.request_started.connect(signal_func)


def my_signal_func(*args, **kwargs):
    print('自定义信号 -> ', *args, **kwargs)


# 自定义信号
my_signal = _signals.signal('my_signal')
my_signal.connect(my_signal_func)


@app.route('/')
@cache.cached(timeout=10)
def test():
    my_signal.send('my_signal')
    time.sleep(5)
    print('current_app.config: ', current_app.config)
    return 'flask server'


# 如果当前模块（py文件）被直接执行（主模块），__name__存储的是__main__
if __name__ == '__main__':
    CORS(app, resources=r'/*')
    # 社区版本配置：
    # 1，debug模式（热更新）
    # 2，host 让同局域网内的其他电脑可以访问本服务，也可以用cmd ipconfig 的IPv4地址
    # 3，port 端口号
    app.run(debug=True, host='0.0.0.0', port=5000)
