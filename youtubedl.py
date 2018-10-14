#!/usr/bin/env python3
"""Download video or audio from YouTube."""
import subprocess
import os
import argparse
import re


DOWNLOAD_DIR = os.path.expanduser("~/Downloads")
DEFAULT_FILENAME = "%(title)s-%(id)s-%(format_id)s.%(ext)s"


def trim_url_to_video_only(url):
    """Remove any timestamping, indexing, and playlist info from youtube URL."""
    re_timestamp = re.compile(r"&t=\d+s")
    re_playlist = re.compile(r"&list=[a-zA-Z0-9_]+")
    re_index = re.compile(r"&index=\d+")
    no_t = re_timestamp.sub("", url)
    no_t_or_list = re_playlist.sub("", no_t)
    no_t_or_list_or_index = re_index.sub("", no_t_or_list)
    return no_t_or_list_or_index


def download_video(url, filename=DEFAULT_FILENAME):
    """Download video from YouTube.
    The url will be cleaned of timestamp, playlist, and playlist index.

    Arguments:
        URL -- link to a youtube video.
        Filename -- Filename to save the video to.
    """
    args = [
        "youtube-dl",
        "-f",
        "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "--merge-output-format",
        "mp4",
        "-o",
        filename,
        trim_url_to_video_only(url),
    ]
    return subprocess.check_call(args)


def download_audio(url, filename=DEFAULT_FILENAME):
    """Download audio from a YouTube video.

    The url will be cleaned of timestamp, playlist, and playlist index.

    Arguments:
        URL -- Link to a youtube video.
        Filename -- Filename to save the audio to.
    """
    args = [
        "youtube-dl",
        "--prefer-ffmpeg",
        "-f",
        "171/251/140/bestaudio",
        "--extract-audio",
        "--audio-format",
        "mp3",
        "--audio-quality",
        "0",
        "-o",
        filename,
        trim_url_to_video_only(url)
    ]
    return subprocess.check_call(args)


def main():
    """Wrapper around download to run from the commandline."""
    parser = argparse.ArgumentParser("youtubedl")
    parser.add_argument("--audio-only", required=False, action="store_true")
    parser.add_argument("--filename", required=False)
    parser.add_argument("URL", nargs='+')
    args = parser.parse_args()
    downloader = download_video
    if args.audio_only:
        downloader = download_audio
    filename = DEFAULT_FILENAME
    if args.filename:
        filename = f"{args.filename}.%(ext)s"
    for url in args.URL:
        downloader(url, filename)


if __name__ == "__main__":
    main()
