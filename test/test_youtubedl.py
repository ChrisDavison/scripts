from scripts.youtubedl import trim_url_to_video_only


def test_trim_url_with_playlist():
    expected = "https://www.youtube.com/watch?v=CcoSRXqAkV4"
    url = "https://www.youtube.com/watch?v=CcoSRXqAkV4&list=WL"
    assert trim_url_to_video_only(url) == expected

def test_trim_url_with_index():
    expected = "https://www.youtube.com/watch?v=CcoSRXqAkV4"
    url = "https://www.youtube.com/watch?v=CcoSRXqAkV4&index=10"
    assert trim_url_to_video_only(url) == expected

def test_trim_url_with_timestamp():
    expected = "https://www.youtube.com/watch?v=CcoSRXqAkV4"
    url = "https://www.youtube.com/watch?v=CcoSRXqAkV4&t=30s"
    assert trim_url_to_video_only(url) == expected