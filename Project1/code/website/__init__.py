from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash



db = SQLAlchemy()
DB_NAME = "database10.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + DB_NAME
    # app.config['JWT_SECRET_KEY'] = 'super-secret'
    app.config['JWT_SECRET_KEY'] = 'super-secret' 
    # db = SQLAlchemy(app)
    jwt = JWTManager(app)

    db.init_app(app)

    from .views import view
    # from .auth import auth

    app.register_blueprint(view, url_prefix='/')
    # app.register_blueprint(auth, url_prefix='/')

    from .models import RegisteredUser

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'view.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return RegisteredUser.query.get(int(id))
    
    

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print('Database created!')