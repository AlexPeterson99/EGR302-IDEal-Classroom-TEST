import time, schedule
from datetime import datetime


def work_please():
    # pull dates from database and fill in instead of hardcoded value
    d = datetime(2020, 3, 11, 10, 50)
    now = datetime.now()
    if (compare_to(d, now) <= 0):
        proof()


def proof():
    print("Yay?!")


def compare_to(date, other):
    if (date.year != other.year):
        return date.year - other.year
    elif (date.month != other.month):
        return date.month - other.month
    elif (date.day != other.day):
        return date.day - other.day
    elif (date.hour != other.hour):
        return date.hour - other.hour
    elif (date.minute != other.minute):
        return date.minute - other.minute
    else:
        return date.second - other.second
    

d = datetime(2020, 3, 11, 10, 10)
schedule.every(3).hours.do(work_please)

while True:
    schedule.run_pending()
    time.sleep(1)