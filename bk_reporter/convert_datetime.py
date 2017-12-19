# -*- coding: utf-8 -*-
import datetime


def strip_date(string, format_string="%Y-%m-%dT%H:%M:%S.%fZ"):
    """
        Input: datetime string in ISO8601 format
        Output: date of the original string in str format `YYYY-MM-DD`
    """
    if string:
        formatted = datetime.datetime.strptime(string, format_string).date()
    else:
        formatted = "n/a"
    return str(formatted)


def get_week_number_of_date(string, format_string="%Y-%m-%dT%H:%M:%SZ"):
    """
        Input : datetime_str (i.e. "2017-08-07T23:28:48Z")
        Output: "36.2017"
    """
    if string:
        try:
            formatted = datetime.datetime.strptime(
                string,
                format_string).date()
        except ValueError as v_err:
            print("ValueError!")
            raise ValueError(
                "ValueError: input string didn't conform expected format!")
    else:
        print("input string was empty")
        raise ValueError("input string was empty")
    return (
                str(formatted.isocalendar()[1]) +
                "." +
                str(formatted.isocalendar()[0])
            )


if __name__ == '__main__':
    datestr = "2017-08-07T23:28:48Z"
    result = strip_date(datestr, "%Y-%m-%dT%H:%M:%SZ")
    print(result, type(result))
    result = get_week_number_of_date(datestr, "%Y-%m-%dT%H:%M:%SZ")
    print(result, type(result))
