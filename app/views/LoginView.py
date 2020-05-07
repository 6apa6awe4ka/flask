from flask_classy import FlaskView, route
from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_user, login_required, logout_user
from forms import RegistrationForm, LoginForm

import redis


class LoginView(FlaskView):
    def get(self):
        r = redis.Redis(host='redis')
        r.mset({"Croatia": "Zagreb", "Bahamas": "Nassau"})

        if current_user.is_authenticated:
            return redirect(
                url_for('.IndexView:index')
            )
        form = LoginForm()
        return render_template('login.html', form=form, user=current_user)

    def post(self):
        form = LoginForm()
        if not current_user.is_authenticated and form.validate_on_submit():
            login_user(form.user)

        return redirect(
            url_for('.LoginView:')
        )

    def password_restore(self):
        return 'password_restore'

    def resend_confirmation_token(self):
        return 'resend_confirmation_token'