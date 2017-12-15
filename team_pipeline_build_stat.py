#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Running this module can generate a report about how each team adopt the BK
"""
import requests
import json
import os
from exceptions import NoTeamError
from exceptions import GeneralApiError


GQL_QUERY = {"query": '''{
                  organization(slug:"myob") {
                    teams(first:500) {
                      count
                      edges {
                        node {
                          slug
                          pipelines(first:500) {
                            count
                            edges {
                              node {
                                pipeline {
                                  slug
                                  pass_builds:builds(state:PASSED) {
                                    pass_builds_count:count
                                  }

                                  fail_builds:builds(state:FAILED) {
                                    fail_builds_count:count
                                  }

                                  builds(first:1) {
                                    edges {
                                      node {
                                        last_build_time:finishedAt
                                      }
                                    }
                                  }

                                }
                              }
                            }
                          }
                        }
                      }
                    }
                  }
                }'''}


def _team_pipelines(url, auth_token, gql_query):
    """
        Input : BK API token and an Endpoint url
        Output: A list of json result
    """

    headers = {}
    headers['Authorization'] = "Bearer {}".format(auth_token)
    headers['Content-Type'] = 'application/json'
    payload = gql_query
    try:
        resp = requests.post(url, headers=headers, data=json.dumps(payload))
        return resp
    except Exception as err:
        print("SOMETHING WENT WRONG...: ", err)



def get_gql_resp(g_url, dryrun=False, auth_token=""):

    file_path = os.path.join(os.path.dirname(__file__), 'result.json')
    file_exists = os.path.isfile(file_path)

    if file_exists and dryrun:
        print("load json and process data, without running expensive api hit")
        gql_resp = json.load(open('result.json'))
    else:
        print("running expensive api hit")
        r = _team_pipelines(g_url, auth_token, GQL_QUERY)
        if r.status_code == 200:
            try:
                json_resp = r.json()
            except ValueError as ve:
                print(ve)
                raise ValueError
            gql_resp = json_resp
        else:
            raise GeneralApiError(
                "not getting valid reply" +
                "status_code is {}".format(r.status_code))
    if not file_exists and dryrun:
        print("writing json resp to intermediate JSON file")
        with open('result.json', 'w') as out_file:
            json.dump(json_resp, out_file)
    return gql_resp


def process_gql_resp(gql_resp):
    """
        This module processes gql response JSON to get"
                "team_slug"
                "pipe_slug"
                "pass"
                "fail"
                "last"
        Input:  graphQL response JSON
        Output: List of Dictionaries including data for the CSV columns
    """
    teams = gql_resp['data']['organization']['teams']['edges']
    team_count = gql_resp['data']['organization']['teams']['count']
    if team_count < 1:
        raise NoTeamError("Critical: there should be at least 1 team")
    result = []
    for team in teams:
        team_slug = team['node']['slug']
        team_pipelines = team['node']['pipelines']
        for team_pipe in team_pipelines['edges']:
            team_pipe_details = team_pipe['node']['pipeline']
            if not team_pipe_details['builds']['edges']:
                last_build_time = "n/a"
            else:
                last_build_time = team_pipe_details['builds']['edges'][0]['node']['last_build_time']
            result.append({
                "team_slug": team_slug,
                "pipe_slug": team_pipe_details['slug'],
                "pass": team_pipe_details['pass_builds']['pass_builds_count'],
                "fail": team_pipe_details['fail_builds']['fail_builds_count'],
                "last": last_build_time
                })
    return result

