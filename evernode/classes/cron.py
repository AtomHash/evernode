"""
    Cron class to schedule jobs to be done
"""

import datetime
import time
import schedule
from threading import Thread
from .singleton import Singleton


class Cron(metaclass=Singleton):
    """
        All you need to do is init Cron class:
            cron = Cron()
        Then add tasks to schedule
            cron.schedule.every(1).seconds.do(test_job)
    """

    schedule = schedule
    start_time = None
    __enabled = False

    def __init__(self):
        self.start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__start()

    def running(self):
        """ Display running time and if Cron was enabled """
        print('Running since: ' + self.start_time)
        return self.__enabled

    def __loop(self):
        """ Run tasks forever """
        while True:
            self.schedule.run_pending()
            time.sleep(1)

    def __start(self):
        """ Start a new thread to process Cron """
        thread = Thread(target=self.__loop, args=())
        thread.daemon = True  # daemonize thread
        thread.start()
        self.__enabled = True
