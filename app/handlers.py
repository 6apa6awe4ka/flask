import logging
from flask import g, render_template
from models import User

import dependency_injector.containers as di_cnt
import dependency_injector.providers as di_prv

class DIServices(di_cnt.DeclarativeContainer):
    db_session_manager = di_prv.Provider()

def load_user(user_id):
    """
    Callback для login_manager.user_loader.
    Загружает по id информацию о пользователе из БД.
    :param user_id:
    :return model.user.User: объект с текущим пользователем
    """
    return g.db_session.query(User).get(user_id)

def before_request():
    """
    Глобальный before_request, вызываемый перед всеми запросами
    """
    g.db_session = DIServices.db_session_manager()()
    g.db_data = {}

def teardown_app_context(error):
    """
    Вызывается для освобождения конктекста.
    Убиваем сессию во время завершения запроса.
    """
    if error:
        logging.getLogger().exception(
            'Возникла ошибка при обработке запроса'
        )

    if g.get('db_session'):
        try:
            DIServices.db_session_manager().remove()
        except Exception:
            logging.getLogger().exception(
                'Возникла ошибка во время попытки удалить сессию с БД'
            )

def error_404(error):
    return '404 error'


def default_error_handler(error):
    logging.getLogger().exception(
        'Возникла непредвиденная ошибка при обработке запроса'
    )
    return 'exception.html'
    # return render_template('exception.html')

# ------------------------------------------------------------

def after_request(request):
    # request.set_cookie('username', 'the username')
    return request

