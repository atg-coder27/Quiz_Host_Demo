from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from . import quiz_schedule


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(quiz_schedule.schedule,'interval',seconds = 10)
    scheduler.start()