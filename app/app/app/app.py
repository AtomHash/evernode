"""
Provides an entrypoint for for uWSGI
sets up a flask app with defaults from App.py
"""
from evernode.classes import App, JsonResponse
from evernode.models import db

# --- @boot ---
app_class = App(__name__)
app = app_class.app
# --- @boot ---


@app.errorhandler(404)
def page_not_found(e, environ=None):
    return JsonResponse(404, environ=environ)


@app.teardown_request
def teardown_request(exception=None):
    """ do on request tear down """
    if db.session is not None:
        db.session.close()


@app.teardown_appcontext
def teardown_app(exception=None):
    """ do on app tear down """
    pass


# uWSGI entry point
if __name__ == '__main__':
    if app.config['DEBUG']:
        app_class.load_modules(True)
    app.run()
