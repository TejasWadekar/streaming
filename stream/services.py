from __future__ import absolute_import, unicode_literals

import io
import logging
import requests



import tempfile
logger = logging.getLogger("interview")


def stream_video(url):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    return io.BytesIO(response.content)


def generate_video_stream(video_buffer):
    chunk_size = 1024 * 1024  # 1MB chunks
    while True:
        data = video_buffer.read(chunk_size)
        if not data:
            break
        yield data


def stream_video_to_tempfile(url):
    response = requests.get(url, stream=True)
    response.raise_for_status()
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".webm")
    for chunk in response.iter_content(chunk_size=8192):
        if chunk:
            temp_file.write(chunk)
    temp_file.seek(0)
    return temp_file.name
