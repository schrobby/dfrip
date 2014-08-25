#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from os import path
from bs4 import BeautifulSoup
import requests
import json
import re

__version__ = "0.1"

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
    if not response["url"]:
        raise ValueError("The subtitles for this episode are currently being worked on")
    else: return response["url"]

def download_subs(url):
    r = requests.get(url)
    return r.text

def download_file_to(url, file_path):
    r = requests.get(url, stream=True)
    with open(file_path, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()
    return file_path

def save_to_disk(filename, content):
    with open(filename, "wb") as f:
        f.write(content.encode("utf-8"))

def xml_to_srt(xml_subs):
    # XML to SRT Python implementation inspired by Hubwub's PyXMLtoSRT
    # https://github.com/hubwub/PyXMLtoSRT/

    xml_subs = re.sub(r"\n +", "\n", xml_subs)
    soup = BeautifulSoup(xml_subs)

    parse_time = lambda time: time.replace('.', ',')
    srt = ''

    for div_tag in soup.findAll('div'):
        for i, p_tag in enumerate(div_tag.findAll('p')):
            
            srt += str(i + 1) + '\n'
            srt += "%s --> %s\n" % (parse_time(p_tag.get('begin')), parse_time(p_tag.get('end')))

            line = p_tag.text.strip('\n')
            if "<i>" in line and not "</i>" in line:
                line += "</i>"

            srt += line + '\n\n'

    return srt

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Download subtitles from DramaFever and convert them into TTML or SRT.", \
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("series_id", metavar="SERIES", type=int, help="the ID of the series (usually four-digit number)")
    parser.add_argument("episode_num", metavar="EPISODE", type=int, help="the number of the episode")
    parser.add_argument("-f", "--format", choices=["srt", "ttml", "xml"], default="xml", help="the format the subtitles will be saved in")
    parser.add_argument("-o", "--out", metavar="FILENAME", default=".", help="location of the output file or filename")
    parser.add_argument("-v", "--verbose", action="store_true", help="increases output verbosity")

    args = parser.parse_args()

    if args.verbose: print("DramaFever Subtitle Ripper v" + __version__)

    try:
        series = get_series(args.series_id)
        subs_url = get_subs_url(args.series_id, args.episode_num)
    except (ValueError, e):
        print("Error: " + str(e))
        quit()

    print("Series: %s, %s" % (series["name"], series["native_lang_title"]))
    if args.verbose:
        print("Description: " + series["description_short"])
        print("URL: http://www.dramafever.com" + series["www_url"])

    print("\nDownloading subtitle file ...")
    subs = download_subs(subs_url)
    filename = subs_url.split('/')[-1]
    if args.format == "srt": 
        subs = xml_to_srt(subs)
        filename = filename.split('.')[0] + ".srt"

    if args.out:
        filename = args.out + '/' + filename if path.isdir(args.out) else args.out

    print("Saving file as " + filename)
    save_to_disk(filename, subs) 
