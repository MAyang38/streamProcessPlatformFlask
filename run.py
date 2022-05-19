'''
-------------------------------------------------
    File name:    run.py
    Description:    启动flask


-------------------------------------------------
   Version:    v1.0

'''

from app import app

if __name__ == "__main__":
    # from werkzeug.middleware.proxy_fix import ProxyFix
    # app.wsgi_app = ProxyFix(app.wsgi_app)
    app.run()