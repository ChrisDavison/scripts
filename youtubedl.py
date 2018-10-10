#!/usr/bin/env python3
"""Download video or audio from YouTube."""
import subprocess
import os
import argparse
import re

DOWNLOAD_DIR = os.path.expanduser("~/Downloads")


def trim_url_to_video_only(url):
    """Remove any timestamping, indexing, and playlist info from youtube URL."""
    re_timestamp = re.compile(r"&t=\d+s")
    re_playlist = re.compile(r"&list=[a-zA-Z0-9_]{34}")
    re_index = re.compile(r"&index=\d+")
    no_t = re_timestamp.sub("", url)
    no_t_or_list = re_playlist.sub("", no_t)
    no_t_or_list_or_index = re_index.sub("", no_t_or_list)
    return no_t_or_list_or_index


def download(url, *, audio_only=False, prefix=None):
    """Download video or audio from YouTube.

    Arguments:
        URL -- link to a youtube video.  Playlist hash & index, and timestamp, will be removed.

    Keyword Arguments:
        audio_only -- only download the audio
        prefix -- string prefix to prepend to filename (e.g. if you want the video author)
    """
    tidied_url = trim_url_to_video_only(url)
    prefix = f"{prefix}--" if prefix else ""
    arglists = {
        "audio": [
            "youtube-dl",
            "--prefer-ffmpeg",
            "-f",
            "171/251/140/bestaudio",
            "--extract-audio",
            "--audio-format",
            "mp3",
            "--audio-quality",
            "0",
        ],
        "video": [
            "youtube-dl",
            "-f",
            "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "--merge-output-format",
            "mp4",
            "-o",
            f"{prefix}%(title)s-%(id)s-%(format_id)s.%(ext)s",
        ],
    }
    args = arglists["audio"] if audio_only else arglists["video"]
    args.append(tidied_url)
    subprocess.check_call(args)


def main():
    """Wrapper around download to run from the commandline."""
    parser = argparse.ArgumentParser("youtubedl")
    parser.add_argument("--audio-only", required=False, action="store_true")
    parser.add_argument("--prefix", required=False)
    parser.add_argument("URL")
    args = parser.parse_args()
    download(args.URL, audio_only=args.audio_only, prefix=args.prefix)


if __name__ == "__main__":
    main()
