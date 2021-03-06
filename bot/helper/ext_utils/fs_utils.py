import sys
from bot import aria2, LOGGER, DOWNLOAD_DIR
import shutil
import os
import pathlib
import mimetypes
import tarfile


def clean_download(path: str):
    if os.path.exists(path):
        LOGGER.info(f"Cleaning download: {path}")
        shutil.rmtree(path)


def start_cleanup():
    try:
        shutil.rmtree(DOWNLOAD_DIR)
    except FileNotFoundError:
        pass


def exit_clean_up(signal, frame):
    try:
        LOGGER.info("Please wait, while we clean up the downloads and stop running downloads")
        aria2.remove_all(True)
        shutil.rmtree(DOWNLOAD_DIR)
        sys.exit(0)
    except KeyboardInterrupt:
        LOGGER.warning("Force Exiting before the cleanup finishes!")
        sys.exit(1)


def tar(org_path):
    tar_path = org_path + ".tar"
    path = pathlib.PurePath(org_path)
    LOGGER.info(f'Tar: orig_path: {org_path}, tar_path: {tar_path}')
    tar = tarfile.open(tar_path, "w")
    tar.add(org_path,arcname=path.name)
    tar.close()
    return tar_path


def get_mime_type(file_path):
    mime_type = mimetypes.guess_type(file_path)[0]
    mime_type = mime_type if mime_type else "text/plain"
    return mime_type
