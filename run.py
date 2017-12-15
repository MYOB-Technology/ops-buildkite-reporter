#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
from settings import setup_essential_var
from settings import GRAPHQL_URL
from team_pipeline_build_stat import get_gql_resp
from team_pipeline_build_stat import process_gql_resp
from builds_per_day import get_builds_per_day
from csv_ops import ProcessCsvFile

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


try:
    gql_resp = get_gql_resp(GRAPHQL_URL, var_dict["DRYRUN"], var_dict["TOKEN"])
except ValueError as err:
        print(err)
processed_data = process_gql_resp(gql_resp)
# for item in processed_data:
#     print(item["team_slug"], item["pipe_slug"])
# print(len(processed_data))
builds_per_day = get_builds_per_day(processed_data)


# # csv-ops
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

# csv-ops
p = ProcessCsvFile(".")
p.prepare_result_file()
p.write_csv_header([
    "team",
    "pipeline",
    "date",
    "builds_count",
    ])
for data in builds_per_day:
    p.write_csv([
        data["team"],
        data["pipe"],
        data["date"],
        data["builds_count"],
    ])
