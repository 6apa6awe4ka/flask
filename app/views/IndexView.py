from flask_classy import FlaskView, route

class IndexView(FlaskView):
    def index(self):
        return '/test/'