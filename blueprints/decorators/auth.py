from flask import session, redirect
import functools


def login_auth(func):
    """
    写上 @functools.wraps(func)，打印 login
    不写 @functools.wraps(func)，打印 inner
    总结 写上，被装饰的函数名就是其本身
    """
    @functools.wraps(func)
    def auth(*args, **kwargs):
        if session.get('session_id', None):
            return func(*args, **kwargs)
        else:
            return redirect('/login')

    return auth
