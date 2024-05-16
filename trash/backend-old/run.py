'''
THIS IS THE MAIN RUN FILE
'''

from user.main import app as user_app
from gpt.main import app as gpt_app

from werkzeug.middleware.dispatcher import DispatcherMiddleware # use to combine each Flask app into a larger one that is dispatched based on prefix
from werkzeug.serving import run_simple # werkzeug development server

from flask_cors import CORS

# user app runs on normal endpoint
# the others must run on modified endpoints

application = DispatcherMiddleware(user_app, {'/gpt': gpt_app})

# user app is the default

# so need /gpt after the port for gpt (e.g. localhost:5000/gpt)
# application = DispatcherMiddleware(flask_app_1, {'/1': flask_app_2, '/2': flask_app_3})

if __name__ == "__main__":
    run_simple('localhost', 5000, application, use_reloader=True, use_debugger=True, use_evalex=True, threaded=True)
    # need to enable multithreading otherwise it gets stuck