import os
import shutil
import tempfile
import subprocess
import logging

from django.db import models
from django.core.files import File

def _ffmpeg_compress(in_path: str, out_path: str) -> None:
    """
    Сжимает видео в MP4 (H.264/AAC).
    - scale: ограничиваем ширину до 1280 (720p/1080p лайк), высота авто, кратность 2
    - crf: качество (чем больше, тем сильнее сжатие). 26–30 обычно норм. Поставил 28.
    - preset: скорость/качество (fast/veryfast — норм для сервера)
    - +faststart: чтобы видео быстро начинало играть в браузере
    """
    cmd = [
        "ffmpeg",
        "-y",
        "-i", in_path,
        "-vf", "scale='min(1280,iw)':-2",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "28",
        "-c:a", "aac",
        "-b:a", "128k",
        "-movflags", "+faststart",
        out_path,
    ]
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)


def _get_local_input_path(file_field) -> tuple[str, str | None]:
    """
    Возвращает (in_path, tmp_in_path_to_delete)
    Если storage даёт file.path — берём его.
    Иначе скачиваем во временный файл и отдаём путь.
    """
    try:
        return file_field.path, None
    except Exception:
        tmp_in = tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file_field.name)[1] or ".mp4")
        tmp_in.close()

        file_field.open("rb")
        try:
            with open(tmp_in.name, "wb") as f:
                for chunk in file_field.chunks():
                    f.write(chunk)
        finally:
            file_field.close()

        return tmp_in.name, tmp_in.name