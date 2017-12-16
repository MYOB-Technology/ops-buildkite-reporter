#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from settings import (
    setup_essential_var,
    GRAPHQL_URL,
    REST_API_URL)
# import custom utils
from bk_reporter.gql_utils import get_gql_resp
from bk_reporter.csv_ops import ProcessCsvFile
# 1st feature delivery
from bk_reporter.team_pipeline_build_stat import (
    GQL_QUERY_TEAM_PIPE_BUILD,
    get_team_pipe_build_stat)
# 2nd feature delivery
from bk_reporter.builds_per_day import get_builds_per_day
# 3rd feature delivery
from bk_reporter.period_build_stat import iterate_period_for_builds


# setup logging


# get key program parameter ready
key_list = ["TOKEN", "DRYRUN", "LAMBDA"]
var_dict = setup_essential_var()

# if it is running in AWS-LAMBDA, we want program dependencies in zip(./vendor)
if var_dict["LAMBDA"]:
    print("I am running in AWS-LAMBDA")
    # to ensure installed dep in ./vendor can be imported
    sys.path.append(os.path.join(os.getcwd(), "vendor"))
else:
    print("I am NOT running in AWS-LAMBDA")


# try:
#     gql_resp = get_gql_resp(GRAPHQL_URL, GQL_QUERY_TEAM_PIPE_BUILD, var_dict["DRYRUN"], var_dict["TOKEN"])
# except ValueError as err:
#         print(err)
# processed_data = get_team_pipe_build_stat(gql_resp)
## 2nd feature delivery
# builds_per_day = get_builds_per_day(processed_data, REST_API_URL)

# # csv-ops-I
# p = ProcessCsvFile(".")
# p.prepare_result_file()
# p.write_csv_header([
#     "team",
#     "pipeline",
#     "pass_builds",
#     "failed_builds",
#     "last_used"
#     ])
# for data in processed_data:
#     p.write_csv([
#         data["team_slug"],
#         data["pipe_slug"],
#         data["pass"],
#         data["fail"],
#         data["last"]
#     ])

# csv-ops-II
# p = ProcessCsvFile(".")
# p.prepare_result_file()
# p.write_csv_header([
#     "team",
#     "pipeline",
#     "date",
#     "builds_count",
#     ])
# for data in builds_per_day:
#     p.write_csv([
#         data["team"],
#         data["pipe"],
#         data["date"],
#         data["builds_count"],
#     ])


## 3rd delivery:
## input example for FUNC "iterate_period_for_builds"
# org_slug = '"myob"'
# week_start = '"2017-08-07T23:28:48Z"'
# week_end = '"2017-08-14T23:28:48Z"'
period_build_count = iterate_period_for_builds(2017, '"myob"', GRAPHQL_URL, var_dict["DRYRUN"], var_dict["TOKEN"])

# csv-ops-III
p = ProcessCsvFile(".")
p.prepare_result_file()
p.write_csv_header([
    "week",
    "passed_builds",
    "failed_builds",
    ])
for data in period_build_count:
    p.write_csv([
        data["week"],
        data["pass_build"],
        data["fail_build"],
    ])
