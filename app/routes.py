from os.path import join
from flask import Blueprint
import views
from config import config

app_blueprint = Blueprint(
    '', __name__,
    template_folder=join(config.BASE_DIR, 'templates'),
    static_url_path='/static', static_folder='static'
)

views.IndexView.register(app_blueprint, route_base='/')
views.LoginView.register(app_blueprint)
views.RegistrationView.register(app_blueprint)
views.TestView.register(app_blueprint)