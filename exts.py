from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_caching import Cache

# 实例化数据库
db = SQLAlchemy()
# 实例化数据库迁移
migrate = Migrate()
# 实例化缓存对象
cache = Cache()


# 所有第三方插件与app绑定
def init_plugins(app):
    db.init_app(app=app)
    migrate.init_app(app=app, db=db)
    cache.init_app(app=app, config={
        'CACHE_TYPE': 'simple'
    })
