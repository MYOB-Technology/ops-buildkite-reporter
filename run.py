#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
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

from bk_reporter.period_build_stat import convert_list_to_dict
from bk_reporter.weekly_count import *


def main():

    # get key program parameter ready
    key_list = ["TOKEN", "DRYRUN", "LAMBDA"]
    var_dict = setup_essential_var()


    # setup logging
    log_config = {
        'format': '[%(asctime)s] %(message)s',
        'datefmt': '%m/%d/%Y %H:%M:%S',
        'level': logging.DEBUG if var_dict['DEBUG'] else logging.INFO,
        'stream': sys.stdout,
    }
    logging.basicConfig(**log_config)
    logging.getLogger().setLevel(logging.DEBUG)
    LOGGER = logging.getLogger(__name__)
    LOGGER.debug("bk usage reporter stating! ")


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

    years = [2016, 2017]
    # years = [2017]
    period_build_count = []
    for year in years:
        period_build_count += (
            iterate_period_for_builds(
                year,
                '"myob"',
                GRAPHQL_URL,
                var_dict["DRYRUN"],
                var_dict["TOKEN"]))

    ## user facing params going to feed-in to `weekly_count` module
    weekly_count_params = [{
            "query": GQL_QUERY_WEEKLY_COUNT_PIPE,
            "topic": "pipelines"
        },
        {
            "query": GQL_QUERY_WEEKLY_COUNT_TEAM,
            "topic": "teams"
        }]

    for query_topic in weekly_count_params:
        gql_data = access_createdAt_date(
            GRAPHQL_URL,
            query_topic["query"],
            var_dict["TOKEN"],
            query_topic["topic"])
        weekly_stat = generate_weekly_stat(gql_data)
        accumulated_stat = get_accumulated_weekly_stat(weekly_stat)
        # csv_ready_data = prepare_data_for_csv(accumulated_stat, query_topic["topic"])
        period_build_count = join_results(
            accumulated_stat,
            period_build_count,
            query_topic["topic"])
    print(period_build_count)


    # csv-ops-III
    p = ProcessCsvFile(".")
    p.prepare_result_file()
    p.write_csv_header([
        "week",
        "pass_build",
        "fail_build",
        "pipelines",
        "teams"
        ])
    for data in period_build_count:
        p.write_csv([
            data["week"],
            data["pass_build"],
            data["fail_build"],
            data["pipelines"],
            data["teams"],
        ])


if __name__ == "__main__":
    main()

    # experimental...

    # get key program parameter ready
    # key_list = ["TOKEN", "DRYRUN", "LAMBDA"]
    # var_dict = setup_essential_var()

    # from bk_reporter.weekly_count import *

    # # # user facing params going to feed-in to `weekly_count` module
    # weekly_count_params = [{
    #         "query": GQL_QUERY_WEEKLY_COUNT_PIPE,
    #         "topic": "pipelines"
    #     },
    #     {
    #         "query": GQL_QUERY_WEEKLY_COUNT_TEAM,
    #         "topic": "teams"
    #     }]

    # for query_topic in weekly_count_params:
    #     gql_data = access_createdAt_date(
    #         GRAPHQL_URL,
    #         query_topic["query"],
    #         var_dict["TOKEN"],
    #         query_topic["topic"])
    #     weekly_stat = generate_weekly_stat(gql_data)
    #     accumulated_stat = get_accumulated_weekly_stat(weekly_stat)
    #     csv_ready_data = prepare_data_for_csv(accumulated_stat, query_topic["topic"])

    #     from bk_reporter.weekly_count import join_results
    #     result = join_results(csv_ready_data, period_build_count)
    #     print(result)

        # csv_process = ProcessCsvFile(".")
        # csv_process.prepare_result_file(query_topic["topic"])
        # csv_process.write_csv_header([
        #     "week",
        #     query_topic["topic"],
        #     ])
        # for data in csv_ready_data:
        #     csv_process.write_csv([
        #         data["week"],
        #         data[query_topic["topic"]],
        #     ])
