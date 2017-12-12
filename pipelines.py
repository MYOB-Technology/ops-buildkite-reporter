#!/usr/bin/env python3
from api import get_data
import os
import datetime
from csv_ops import ProcessCsvFile


if __name__ == '__main__':

    url = "https://api.buildkite.com/v2/organizations/myob/pipelines"
    pipelines = get_data(url,100)

    # csv ops
    write_csv = ProcessCsvFile('.')
    write_csv.prepare_result_file()
    write_csv.write_csv_header(['slug', 'created_at'])
    for pipe in pipelines:
        write_csv.write_csv([pipe['slug'], pipe['created_at']])
