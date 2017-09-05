from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db=SQLAlchemy()
login_manager=LoginManager()

login_manager.session_protection = 'strong'
login_manager.login_view = '/login'

def create_app(config):
    app = Flask(__name__,static_folder='static',template_folder='templates')
    # 加载配置文件
    app.config.from_object(config)
    # 初始化
    db.init_app(app)
    login_manager.init_app(app)
    # 蓝图
    from .views.user import user as user_blueprint
    app.register_blueprint(user_blueprint)
    from .views.api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    return app