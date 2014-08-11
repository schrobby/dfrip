#!/usr/bin/python

import requests
import json
from os import path
import sys

API_BASE = "http://www.dramafever.com/api/4"
API_CS_V4 = "DA59dtVXYLxajktV"

def api_call(url, **kwargs):
    kwargs.update({'cs': API_CS_V4})
    r = requests.get(API_BASE + url, params=kwargs)

    if r.status_code != 200:
        raise ValueError("Invalid or unkonwn API call")

    response = json.loads(r.text)
    if "type" in response.keys() and response["type"] == "Error":
        raise ValueError(response["message"])

    return response

def get_series(series_id):
    response = api_call("/series/query/", series_id=series_id)
    return response["series"][str(series_id)]

def get_subs_url(series_id, episode_num, lang="en", format="dfxp", file_format="dfxp"):
    response = api_call("/episode/subtitle/", series_id=series_id, number=episode_num, \
        lang=lang, format=format, file_format=file_format)
    return response["url"]

def download_file_to(url, file_path):
    r = requests.get(url, stream=True)
    with open(file_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
    return file_path

if __name__ == "__main__":
    series = sys.argv[1]
    episode = sys.argv[2]

    url = get_subs_url(series, episode)
    print("Series: " + get_series(series)["name"])
    print("URL: " + url)
    print("Saving file as " + url.split('/')[-1])

    download_file_to(url, url.split('/')[-1])



