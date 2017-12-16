# -*- coding: utf-8 -*-
from bk_reporter.rest_api_utils import get_data
from bk_reporter.convert_datetime import strip_date
from itertools import groupby


def _get_pipeline(processed_gql_data):
    """
        Input : processed_gql_data
        Output: [{team:team_slug, pipelines:pipeline_slug}]
    """
    # team_pipe_dict = []
    # for data in processed_gql_data:
    #     new_dict.append({key:data[key] for key in ("team_slug", "pipe_slug")})
    # return team_pipe_dict
    return [
        {key:data[key] for key in ("team_slug", "pipe_slug")}
        for data in processed_gql_data
        ]


def _get_builds_from_pipeline(pipeline_slug, rest_api_url):
    """
        Input : [pipeline-slug]
        Output: [{date: daily_build_count}]
    """
    build_url = rest_api_url + "/{}/builds".format(pipeline_slug)
    print("build_url", build_url)
    try:
        resp = get_data(build_url,100)
    except TypeError:
        print("resp might be empty? ")
        raise TypeError
    finished_datetime = [strip_date(item['finished_at']) for item in resp]
    result = [{key:len(list(group))} for key, group in groupby(finished_datetime)]
    return result


def get_builds_per_day(processed_gql_data, rest_api_url):
    """
        Main func of this module, depends on processed-data generated
        by team_pipeline_build_stat module

        Input : processed_gql_data
        Output: [{team:team, pipeline:pipeline, date:date, builds_count}]
    """
    # print(_get_pipeline(processed_gql_data))
    pipelines = _get_pipeline(processed_gql_data)
    team_pipe_buildcount = []
    for pipe in pipelines:
        date_build_count = _get_builds_from_pipeline(pipe["pipe_slug"], rest_api_url)
        for item_date_build_count in date_build_count:
            team_pipe_buildcount.append({
                "team":pipe["team_slug"],
                "pipe":pipe["pipe_slug"],
                "date":list(item_date_build_count.keys())[0],
                "builds_count":list(item_date_build_count.values())[0]
                })
        [print(item) for item in team_pipe_buildcount]
    return team_pipe_buildcount
