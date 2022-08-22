""" This script is used to download videos from youtube.

It uses python hydra package to set up the configuration.
The playlist can be defined in a yaml file. Please refer to
[scripts/video_downloader/conf/playlist/nba_courts.yaml] as an example

Usage:
source activate.sh (activate.ps1 on Windows)
python ./script/video_download/download_youtube_video.py playlist <your-playlist-yaml-file>

The mp4 video files will be saved under output directory specified in the playlist
yaml file.
"""
import shutil
from pytube import YouTube, Stream
import os
import hydra
from omegaconf import DictConfig, OmegaConf
import threading
from glob import glob
import moviepy.editor as me


def progress_callback(stream: Stream, chunk, bytes_remain):
    file = stream.get_file_path()
    print(f"[{file}] - data remaining: {bytes_remain/1e6: .4f} MBytes", end="\r")


def complete_callback(stream: Stream, file_path):
    print(f"[{file_path}] - download completed!")


def check_basename_exist(out_dir: str, basename: str):
    """Check if any file with the same basename already exists in the out_dir"""
    flist = glob(os.path.join(out_dir, f"{basename}*"))
    found = False
    for fn in flist:
        if fn.find(basename) >= 0:
            found = True
            break
    return found


def download_youtube(videourl, out_dir, new_video_name=None, convert_to_mp3=False):
    """Download youtube video."""
    # === construct youtube object
    yt = YouTube(
        videourl,
        on_progress_callback=progress_callback,
        on_complete_callback=complete_callback
    )
    yt = yt.streams.filter(
        progressive=True, file_extension='mp4').order_by('resolution').desc().first()

    # === create the output directory if not exists
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    # === check if file already exists, if so, exit
    if check_basename_exist(out_dir, new_video_name):
        return

    # video file does not exist, download now...
    yt.download(out_dir)

    # === rename the video file name to the specified one
    src = os.path.join(out_dir, yt.default_filename)
    if new_video_name:
        dir = os.path.dirname(src)
        filename = os.path.basename(src)
        basename, ext = os.path.splitext(filename)
        dst = os.path.join(dir, f"{new_video_name}{ext}")
        shutil.move(src, dst)
    else:
        dst = src  # no-renaming
    
    # === convert to mp3
    if convert_to_mp3:
        video = me.VideoFileClip(dst)
        dir = os.path.dirname(dst)
        full_basename = os.path.basename(dst)
        basename, ext = os.path.splitext(full_basename)
        new_dir = os.path.join(dir, "mp3/")
        if not os.path.isdir(new_dir):
            os.makedirs(new_dir)
        mp3file = os.path.join(new_dir,f"{basename}.mp3")
        video.audio.write_audiofile(mp3file)

@hydra.main(version_base=None, config_path="conf", config_name="config")
def main(cfg: DictConfig):
    # === parse configurations
    yt_paths = cfg.playlist.youtube_paths
    out_dir = cfg.playlist.out_dir
    convert_to_mp3 = cfg.playlist.convert_to_mp3

    # === download videos in multiple threads
    thread_list = []
    for item in yt_paths:
        ytpath = item[0]
        out_file = item[1]
        out_file = None if out_file == "" else out_file

        thread_list.append(
            threading.Thread(
                target=download_youtube,
                args=[ytpath, out_dir, out_file, convert_to_mp3]
            )
        )

    for thr in thread_list:
        thr.start()
    for thr in thread_list:
        thr.join()

    print("\nDownload Completed!!")


if __name__ == "__main__":
    main()
