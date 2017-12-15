# -*- coding: utf-8 -*-
from api import get_data
from convert_datetime import strip_date
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


def _get_builds_from_pipeline(pipeline_slug):
    """
        Input : [pipeline-slug]
        Output: [{date: daily_build_count}]
    """
    build_url = "https://api.buildkite.com/v2/organizations/myob/pipelines/{}/builds".format(pipeline_slug)
    print("build_url", build_url)
    try:
        resp = get_data(build_url,100)
    except TypeError:
        print("resp might be empty? ")
        raise TypeError
    finished_datetime = [strip_date(item['finished_at']) for item in resp]
    result = [{key:len(list(group))} for key, group in groupby(finished_datetime)]
    return result


def get_builds_per_day(processed_gql_data):
    """
        Input : processed_gql_data
        Output: [{team:team, pipeline:pipeline, date:date, builds_count}]
    """
    # print(_get_pipeline(processed_gql_data))
    pipelines = _get_pipeline(processed_gql_data)
    team_pipe_buildcount = []
    for pipe in pipelines:
        date_build_count = _get_builds_from_pipeline(pipe["pipe_slug"])
        for item_date_build_count in date_build_count:
            # print(item_date_build_count, type(item_date_build_count))
            # for key, value in item_date_build_count.iteritems():
            #     print(key, value)
            # import sys
            # sys.exit(0)
            team_pipe_buildcount.append({
                "team":pipe["team_slug"],
                "pipe":pipe["pipe_slug"],
                "date":list(item_date_build_count.keys())[0],
                "builds_count":list(item_date_build_count.values())[0]
                })
        [print(item) for item in team_pipe_buildcount]

    # [print(item) for item in team_pipe_buildcount]
    return team_pipe_buildcount
