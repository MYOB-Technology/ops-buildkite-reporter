#!/usr/bin/env python3
import requests
import os,re
from exceptions import ApiTokenError

def get_data(token, url, per_page=100):
    """
        Input: BK API token and an Endpoint
        Output: A list of json result from all pages in the pagination
    """
    headers = {'Authorization': "Bearer " + token}
    params = {}
    params["per_page"] = per_page
    result = []

    # init pagination loop
    page_count = 1
    last_url_exists = True
    try:
        while last_url_exists:
            resp = _hit_api(url, headers, params, page_count)
            page_count += 1
            # exit if it had reached the last page
            if not 'last' in resp.links:
                last_url_exists = False
            if resp.status_code == 200:
                result += resp.json()
            elif resp.status_code == 401:
                raise ApiTokenError(resp.status_code,"token is not valid at all")
            elif resp.status_code == 403:
                raise ApiTokenError(resp.status_code,"insufficient token scope")
        print(len(result))
        return result
    except Exception as e:
        print("SOMETHING WAS WRONG: ", e)

def _hit_api(url, headers, params, page_count):
    params["page"] = str(page_count)
    try:
        resp = requests.get(url,headers=headers,params=params)
        return resp
    except Exception as e:
        print("SOMETHING WRONG: hit_api",e)


if __name__ == '__main__':
    token = os.environ['BK_TOKEN']

    url = "https://api.buildkite.com/v2/organizations/myob/pipelines"
    pipelines = get_data(token,url,99)
    # print(len(r))
