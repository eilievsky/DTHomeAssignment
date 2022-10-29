from datetime import datetime as dt

# return date with a format that required for API activation
def return_formatted_date(date_obj):
    tmp_date = dt(date_obj.year, date_obj.month, date_obj.day, 0, 0)
    tmpStr = tmp_date.isoformat()
    return tmpStr + 'Z'