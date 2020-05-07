from flask_classy import FlaskView, route
from staff import get_r
from flask import redirect, url_for, request


class TestView(FlaskView):
    def before_get(self):
        pass

    def after_post(self, response):
        return response

    def get(self):
        # response = redirect(
        #     url_for('.LoginView:get')
        # )
        # response.set_cookie('test','test')
        test = request.cookies.get('test')
        if test:
            return 'test'
        return 'not test'

    def post(self):
        return 'postss'

    @route('1') 
    def test1(self):
        r = get_r()
        r.mset({"Croatia": "Zagreb", "Bahamas": "Nassau"})
        return '1'

    @route('2')
    def test2(self):
        r = get_r()
        return r.get("Croatia")
