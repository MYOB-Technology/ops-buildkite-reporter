# -*- coding: utf-8 -*-
"""
    Running this module can generate a report about how each team adopt the BK
"""


GQL_QUERY_TEAM_PIPE_BUILD = {"query": '''{
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


def get_team_pipe_build_stat(gql_resp):
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
