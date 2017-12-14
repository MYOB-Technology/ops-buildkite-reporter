#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime


def strip_date(string):
    """
        Input: datetime string in ISO8601 format
        Output: date of the original string in str format `YYYY-MM-DD`
    """
    formatted = datetime.datetime.strptime(string, "%Y-%m-%dT%H:%M:%SZ").date()
    return str(formatted)

if __name__ == '__main__':

    datestr = "2017-08-07T23:28:48Z"
    strip_date(datestr)
