"""
Provides an entrypoint for uWSGI
sets up a flask app with defaults from App.py
"""
from datetime import datetime
from flask_migrate import Migrate
from evernode.classes import App, JsonResponse, Cron
from evernode.models import db

# --- @boot ---
evernode_app = App(__name__)
app = evernode_app.app
# --- @boot ---

# migrations
# migrate = Migrate(app, db)

# enable Cron
cron = Cron()

"""
# test cron job
def test_job():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print('cron job executed: ' + now)

def test_jo2():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print('cron job executed - 2: ' + now)


# cron.schedule.every(1).seconds.do(test_job)
# cron.schedule.every(1).minutes.do(test_job)
# cron.schedule.every().minute.at(":00").do(test_job)
cron.schedule.every(1).seconds.do(test_job)

cron2 = Cron()  # does not duplicate task firing
cron.schedule.every(1).seconds.do(test_jo2)

"""


@app.errorhandler(404)
def page_not_found(e, environ=None):
    return JsonResponse(404, environ=environ)


@app.teardown_request
def teardown_request(exception=None):
    """ do on request tear down """
    # if db.session is not None:
        # db.session.close()


@app.teardown_appcontext
def teardown_app(exception=None):
    """ do on app tear down """
    pass


# uWSGI entry point
if __name__ == '__main__':
    app.run()
