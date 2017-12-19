# -*- coding: utf-8 -*-

import requests
import json
import os
from bk_reporter.exceptions import GeneralApiError


def _post_gql_query(url, auth_token, gql_query):
    """
        Low-level plumbing that abstracts of posting GQL queries to url
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


def get_gql_resp(g_url, gql_query, dryrun=False, auth_token=""):

    file_path = os.path.join(os.path.dirname(__file__), 'result.json')
    file_exists = os.path.isfile(file_path)

    if file_exists and dryrun:
        print("load json and process data, without running expensive api hit")
        gql_resp = json.load(open('result.json'))
    else:
        print("running expensive api hit")
        r = _post_gql_query(g_url, auth_token, gql_query)
        if r.status_code == 200:
            try:
                json_resp = r.json()
            except ValueError as ve:
                print(ve)
                raise ValueError
            gql_resp = json_resp
        else:
            print(r.headers)
            raise GeneralApiError(
                "not getting valid reply..." +
                "status_code is {}".format(r.status_code))
    if not file_exists and dryrun:
        print("writing json resp to intermediate JSON file")
        with open('result.json', 'w') as out_file:
            json.dump(json_resp, out_file)
    return gql_resp
