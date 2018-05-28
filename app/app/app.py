"""
Provides an entrypoint for uWSGI
sets up a flask app with defaults from App.py
"""
from flask_migrate import Migrate
from evernode.classes import App, JsonResponse
from evernode.models import db

# --- @boot ---
evernode_app = App(__name__)
app = evernode_app.app
# --- @boot ---

# migrations
migrate = Migrate(app, db)


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
    app.run()
