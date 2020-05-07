from flask_classy import FlaskView, route
from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_user, login_required, logout_user
from forms import RegistrationForm, LoginForm
from repositories import UserRepository

class RegistrationView(FlaskView):

    def get(self):
        if current_user.is_authenticated:
            return redirect(
                url_for('.IndexView:index')
            )
        form = RegistrationForm()

        return render_template(
            'registration.html', form=form, is_success=True
        )

    def post(self):
        form = RegistrationForm()
        is_success = True
        reg_done = False

        if not current_user.is_authenticated and form.validate_on_submit():
            is_success = UserRepository.registration(form)
            if is_success:
                reg_done = True

        return render_template(
            'registration.html', form=form, is_success=is_success, reg_done=reg_done
        )