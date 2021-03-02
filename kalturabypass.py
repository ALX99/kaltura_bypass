import argparse
import re
import sys
from urllib.parse import unquote

import requests
import youtube_dl

video_entry = "https://play.chalmers.se/media/Short+lecture+on+blended+learning+and+flipped+classroom+-+Quiz/0_ax7oyyj9"


def get_cdn() -> str:
    resp = requests.get(video_entry)
    html = resp.content.decode("utf-8")
    matches = re.findall(r'.*cdnUrl = "(.*?\.net)', html)
    if len(matches) == 0:
        raise RuntimeError("Failed to locate CDN url")
    cdn = str(matches[0]).replace("\\", "")
    if len(cdn) == 0:
        raise RuntimeError("Failed to strip backslashes from the CDN url")
    return cdn


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download private videos hosted on the Kaltura video platform for Swedish universities")
    parser.add_argument(
        'url', type=str, help="The url to the private Kaltura video")
    args = parser.parse_args()

    try:
        video_id = re.findall(
            r'entryid/(.*?)/', unquote(args.url) + "/",
            re.IGNORECASE)[0]
    except:
        print("Failed to obtain video id from the provided URL")
        sys.exit(1)

    try:
        print("Trying to locate the CDN")
        cdn = get_cdn()
    except Exception as e:
        print(e)
        sys.exit(1)
    print(f"CDN found at {cdn}")

    dl_link = f"{cdn}/p/333/sp/33300/playManifest/entryId/{video_id}/format/applehttp"
    opts = {'format': 'best', 'outtmpl': f'{video_id}.%(ext)s'}
    print("Downloading video ...")
    with youtube_dl.YoutubeDL(opts) as ydl:
        ydl.download([dl_link])
    print(f"Video saved as {video_id}.mp4!")
