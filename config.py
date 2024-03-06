# 数据库配置信息
HOSTNAME = "127.0.0.1"
PORT = "3306"
DATABASE = "memo"
USERNAME = "root"
PASSWORD = "13724900003"
_db_uri = "mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8"
DB_URI = _db_uri.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
# 禁止对象追踪修改（若开启，性能下降）
SQLALCHEMY_TRACK_MODIFICATIONS = False

# app的配置信息全部在config对象里，但一些常用的配置，被提到app这一层，例如：debug，secret_key

# session配置
# 秘钥
SECRET_KEY = 'abcdef_123456'
# 浏览器记录下的cookie键名
SESSION_COOKIE_NAME = 'session_key'
# 使cookie可以被访问
SESSION_COOKIE_HTTPONLY = False

# 中文不返回ASCII码
JSON_AS_ASCII = False


# 邮箱信息配置

# url接口前缀
url_prefix = '/api'
