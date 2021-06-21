import datetime
from flask import jsonify

def get_date_and_hour():
    now_dt_obj = datetime.datetime.now()
    date = now_dt_obj.strftime("%d of %B %Y")
    time = now_dt_obj.strftime("%H:%M:%S")
    date_and_time = {
        "date": date,
        "time": time
                     }
    return jsonify(date_and_time)


if __name__ == '__main__':
    pass