#!/usr/bin/env python3
import requests
import json
import os,re
from exceptions import NoTeamError, GeneralApiError, EnvVarError

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

def team_pipelines(url):
    """
        Input: BK API token and an Endpoint
        Output: A list of json result of
    """
    token = os.environ['BK_TOKEN']
    headers = {}
    headers['Authorization'] = "Bearer {}".format(token)
    headers['Content-Type'] = 'application/json'

    # result = ""
    params = []
    payload = GQL_QUERY
    try:
        import json
        resp = requests.post(url,headers=headers,data=json.dumps(payload))
        return resp
    except Exception as e:
        print("SOMETHING WRONG: ", e)

def process_gql_resp(gql_resp):
    """
       input: gql_resp in json format
       output: csv file written..
    """
    teams = gql_resp['data']['organization']['teams']['edges']
    team_count = gql_resp['data']['organization']['teams']['count']
    if team_count < 1:
        raise NoTeamError("Critical: there should be at least 1 team")
    # print(type(teams))
    result = []
    for team in teams:
        team_slug = team['node']['slug']
        team_pipelines = team['node']['pipelines']
        # print(team_slug, "|||pipe count=", team_pipelines['count'])
        for team_pipe in team_pipelines['edges']:
            team_pipe_details = team_pipe['node']['pipeline']
            if len(team_pipe_details['builds']['edges']) > 0:
                last_build_time = team_pipe_details['builds']['edges'][0]['node']['last_build_time']
            else:
                last_build_time = "na"
            # print(
            #         team_slug,
            #         team_pipe_details['slug'],
            #         team_pipe_details['pass_builds']['pass_builds_count'],
            #         team_pipe_details['fail_builds']['fail_builds_count'],
            #         last_build_time
            #      )

            result.append({"team_slug": team_slug,
                    "pipe_slug": team_pipe_details['slug'],
                    "pass": team_pipe_details['pass_builds']['pass_builds_count'],
                    "fail": team_pipe_details['fail_builds']['fail_builds_count'],
                    "last": last_build_time
            })
    print("pipeline count within our Org: ", len(result))
    # print(result)
        # team_slug = team['node']['slug']
        # print("pipeline count=",team['node']['pipelines']['count'])
    return result


if __name__ == '__main__':
    if "BK_DRYRUN" in os.environ:
        env_var_dr_value = os.environ['BK_DRYRUN']
        if env_var_dr_value == "True":
            DRYRUN = True
        elif env_var_dr_value == "False":
            DRYRUN = False
        else:
            raise EnvVarError(
                    "expecting string True or False, but got something else"
                )
        print('env var acquired: BK_DRYRUN, value:', DRYRUN)
    else:
        DRYRUN = True

    url = "https://graphql.buildkite.com/v1"
    file_path = os.path.join(os.path.dirname(__file__), 'result.json')
    file_exists = os.path.isfile(file_path)

    if file_exists and DRYRUN:
        print(file_exists, DRYRUN, file_exists and DRYRUN)
        print("load json and process data, without running expensive api hit")
        gql_resp = json.load(open('result.json'))
    else:
        print("running expensive api hit")
        r = team_pipelines(url)
        # print(r.status_code)
        if r.status_code == 200:
            try:
                json_resp = r.json()
            except ValueError as ve:
                print(ve)
                raise ValueError
            gql_resp = json_resp
        else:
            raise GeneralApiError("not getting valid reply")
    if not file_exists and DRYRUN:
        print("writing json resp to intermediate JSON file")
        with open('result.json', 'w') as out_file:
            json.dump(json_resp, out_file)

    processed_data = process_gql_resp(gql_resp)
    from csv_ops import ProcessCsvFile
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

