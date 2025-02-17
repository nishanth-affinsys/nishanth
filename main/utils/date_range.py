from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
import calendar


def get_date_ranges(start, end, frequency):
    start_date = parse(start).date()
    end_date = parse(end).date()
    response = []
    while start_date > end_date:
        res = calendar.monthrange(start_date.year, start_date.month)
        max_date = datetime(start_date.year, start_date.month, res[1]).date()
        sub = max_date - relativedelta(months=frequency - 1)
        min_date = datetime(sub.year, sub.month, 1).date()
        response.insert(0, [min_date, max_date])
        start_date = min_date - relativedelta(days=1)
    return response
