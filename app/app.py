from flask import Flask
from flask_login import LoginManager
from logger import init_logger
from flask_mail import Mail
import handlers
import routes
import logging
from config import config


app = Flask(__name__)
app.config.from_object(config)

# from cli import *
# import os
# from past.builtins import execfile
# def include(filename):
#     if os.path.exists(filename): 
#         execfile(filename)

# include('./cli/vk_parser.py')

init_logger(config.LOGGER_LEVEL)
# flask-login
login_manager = LoginManager(app)
login_manager.login_view = '/auth/'
login_manager.user_loader(handlers.load_user)
# ------------------------------------------------------------------------------------
import itsdangerous
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
db_session_manager = scoped_session(sessionmaker(bind=engine))


import dependency_injector.containers as di_cnt
import dependency_injector.providers as di_prv

mail = Mail(app)

# create providers
class DIServices(di_cnt.DeclarativeContainer):
    db_session_manager = di_prv.Object(db_session_manager)
    mail = di_prv.Object(mail)
    url_serializer = di_prv.Singleton(
        itsdangerous.URLSafeSerializer, secret_key=config.SECRET_KEY
    )


# injection
handlers.DIServices.override(DIServices)
# bulls_and_cows_tasks.DIServices.override(DIServices)
# bulls_and_cows_utils_account.DIServices.override(DIServices)
# ------------------------------------------------------------------------------------
app.register_blueprint(routes.app_blueprint)

app.before_request(handlers.before_request)
app.after_request(handlers.after_request)
app.teardown_appcontext(handlers.teardown_app_context)
app.errorhandler(404)(handlers.error_404)
# app.errorhandler(Exception)(handlers.default_error_handler)

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000, debug=config.DEBUG)