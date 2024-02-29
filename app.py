from flask import Flask, request, signals
from flask.signals import _signals
import config
from flask_migrate import Migrate
from exts import db
from flask_cors import CORS
from models import UserModel

# 导入蓝图
from blueprints.login import bp as login_bp
from blueprints.qa import bp as qa_bp
from blueprints.error import bp as error_bp

app = Flask(__name__)

# CORS(app)

# 给app定配置信息
app.config.from_object(config)
# app.config.from_pyfile('config.py')

# 数据库与app绑定
db.init_app(app)

migrate = Migrate(app, db)

# 注册蓝图
api_prefix = config.url_prefix

app.register_blueprint(login_bp, url_prefix=api_prefix)
app.register_blueprint(qa_bp, url_prefix=api_prefix)
app.register_blueprint(error_bp)

# Flask3.0之后，没有before_first_request
# @app._got_first_request
# def before_first_request_func():
#     # 这里的第一次跟用户和客户端无关，是服务器的第一次
#     print('项目启动初始化一些事情...')


# 请求拦截器（钩子函数 hook）
@app.before_request
def before_request_func():
    print('有人请求', request.path)


# 上下文处理器（钩子函数 hook）
@app.context_processor
def context_processor_func():
    pass


@app.errorhandler(404)
def error_func(err):
    return '自定义错误：%s' % err


def signal_func(*args, **kwargs):
    # *args, **kwargs 形参必须填上
    print('request_started信号 -> ', *args, **kwargs)


# 信号（有很多个，类似于vue的生命周期钩子，如果信号有写代码，就执行，没写代码跳过）
signals.request_started.connect(signal_func)


def my_signal_func(*args, **kwargs):
    print('自定义信号 -> ', *args, **kwargs)


# 自定义信号
my_signal = _signals.signal('my_signal')
my_signal.connect(my_signal_func)


@app.route('/')
def test():
    my_signal.send('my_signal')
    return 'flask server'


# 如果当前模块（py文件）被直接执行（主模块），__name__存储的是__main__
if __name__ == '__main__':
    CORS(app, resources=r'/*')
    # 社区版本配置：
    # 1，debug模式（热更新）
    # 2，host 让其他局域网内的电脑访问本后端项目  也可以用cmd ipconfig 的IPv4地址
    # 3，port 端口号
    app.run(debug=True, host='0.0.0.0', port=5000)
