import json

class EmployeeEncoder(json.JSONEncoder):
        def default(self, o):
            return o.__dict__
import datetime

def json_default(value):
    if isinstance(value, datetime.date):
        return dict(year=value.year, month=value.month, day=value.day)
    else:
        return value.__dict__