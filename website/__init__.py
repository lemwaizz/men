from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "users"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'reject_finance_bill'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://root:password@localhost/{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .admin import admin 
    from .admin_auth import admin_auth  # Import admin and admin_auth blueprints

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(admin_auth, url_prefix='/admin')  # Register admin_auth blueprint

    from .models import User, GarbageCollection

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
