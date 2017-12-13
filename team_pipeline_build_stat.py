#!/usr/bin/env python3
"""
    This module generate reports for the management to monitor BK adoption
"""

import json
import os
from exceptions import NoTeamError, GeneralApiError
from settings import TOKEN, DRYRUN
import requests
from csv_ops import ProcessCsvFile

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
                }'''
            }


def _team_pipelines(url):
    """
        Input: BK API token from Global var and an Endpoint url
        Output: A list of json result of
    """

    headers = {}
    headers['Authorization'] = "Bearer {}".format(TOKEN)
    headers['Content-Type'] = 'application/json'
    payload = GQL_QUERY
    try:
        resp = requests.post(url, headers=headers, data=json.dumps(payload))
        return resp
    except Exception as err:
        print("SOMETHING WENT WRONG...: ", err)


def process_gql_resp(gql_resp):
    """
        This module processes gql response JSON
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


if __name__ == '__main__':
    URL = "https://graphql.buildkite.com/v1"
    FILE_PATH = os.path.join(os.path.dirname(__file__), 'result.json')
    file_exists = os.path.isfile(FILE_PATH)

####################
    if file_exists and DRYRUN:
        print(file_exists, DRYRUN, file_exists and DRYRUN)
        print("load json and process data, without running expensive api hit")
        gql_resp = json.load(open('result.json'))
    else:
        print("running expensive api hit")
        r = _team_pipelines(URL)
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
    if not file_exists and DRYRUN:
        print("writing json resp to intermediate JSON file")
        with open('result.json', 'w') as out_file:
            json.dump(json_resp, out_file)
##################
    processed_data = process_gql_resp(gql_resp)

    p = ProcessCsvFile('.')
    p.prepare_result_file()
    p.write_csv_header([
        'team',
        'pipeline',
        'pass_builds',
        'failed_builds',
        'last_used'
        ])
    for data in processed_data:
        p.write_csv([
            data['team_slug'],
            data['pipe_slug'],
            data['pass'],
            data['fail'],
            data['last']
        ])
