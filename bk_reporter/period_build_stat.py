#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    This moduel helps to calculate number of pass/fail builds created during
    certain period(default: 1 week).

    return [
        {"week": "28.2017", "pass_build": 301, "fail_build": 247}
    ]
"""
# from datetime import datetime
from datetime import datetime
from bk_reporter.gql_utils import get_gql_resp


def _build_gql_query(
    org_slug,
    week_start='"2017-08-07T23:28:48Z"',
    week_end='"2017-08-14T23:28:48Z"'):
    """
        Build GraphQL base on given start/end timestamp of ISO8601 format,
        as well as Org Slug
    """
    query_str = """ {{
                      organization(slug:{0}) {{
                        pipelines(first:500) {{
                          edges {{
                            node {{
                            pass_build:builds(createdAtFrom:{1} createdAtTo:{2} state:PASSED) {{
                                count
                              }}

                            fail_build:builds(createdAtFrom:{1} createdAtTo:{2} state:FAILED) {{
                              count
                              }}
                            }}
                          }}
                        }}
                      }}
                    }}""".format(org_slug, week_start, week_end)
    return {"query": query_str}


def _analyse_builds(gql_resp):
    """
        Analyse gql response for the SUM of passed-builds and failed builds.
    """
    try:
        node_list = gql_resp["data"]["organization"]["pipelines"]["edges"]
    except KeyError as key_err:
        print("maybe gql response was invalid or empty?")
        print(gql_resp)
        raise KeyError
    pass_build = 0
    fail_build = 0
    for node in node_list:
        pass_build += int(node["node"]["pass_build"]["count"])
        fail_build += int(node["node"]["fail_build"]["count"])
    period_build_stat = {"pass_build":pass_build, "fail_build":fail_build}
    print("pass_build", pass_build, "fail_build", fail_build)
    return period_build_stat


def _generate_week_range(year):
    """
        Input : year (2016, 2017 etc)
        Output: [{
            "week": "34.2017",
            "wk_start": '"2017-08-07T00:00:00Z"'
            "wk_end"  : '"2017-08-14T23:59:59Z"'
            }]
    """
    result = []
    this_week = datetime.now().isocalendar()[1]
    for num_week in range(1, 53):
        if num_week > this_week:
            break
        week = "{}.{}".format(num_week, year)
        week_str = str(num_week) + "." + str(year)
        wk_start = '"' + datetime.strptime(
            week +
            "-1", # @Monday of the week
            "%W.%Y-%w"
            ).isoformat(sep="T") + '"'
        wk_end = '"' + datetime.strptime(
            week +
            "-0" + # @Sunday of the week
            "-23-59-59",
            "%W.%Y-%w-%H-%M-%S").isoformat(sep="T") + '"'
        result.append({"week":week_str, "wk_start":wk_start, "wk_end":wk_end })
    # print(result)
    return result


def iterate_period_for_builds(year, org_slug, gql_url, dryrun, token):
    """
        Input : year, org_slug
        Output: {
            "week": <str>, (i.e. "34.2017")
            "pass_build": <datetime>,
            "fail_build": <datetime>
            }
    """
    wk_fences = _generate_week_range(year)
    result = []
    for wk in wk_fences:
        print("iterate_weeks_for_builds:", wk["wk_start"], wk["wk_end"])
        wk_query = _build_gql_query(org_slug, wk["wk_start"], wk["wk_end"])
        gql_resp = get_gql_resp(gql_url, wk_query, dryrun, token)
        analysed_data = _analyse_builds(gql_resp)
        result.append(
                {"week": wk["week"], "pass_build": analysed_data["pass_build"], "fail_build": analysed_data["fail_build"]}
            )
    # print(result)
    return  result


def convert_list_to_dict(dict_array):
    """
        reorganise team-pipe-build-stat list
        from: [
            {week, pass_build, fail_build}
        ]
        to: {
            week: {pass_build, fail_build}
        }
    """
    result = {}
    for dict_item in dict_array:
        week = dict_item["week"]
        result[week] = {
            "pass_build": dict_item["pass_build"],
            "fail_build": dict_item["fail_build"]
        }
    print(result)
    return result
