from pytubefix import YouTube
from pytubefix.cli import on_progress
import pandas as pd
from pathlib import Path
from tqdm import tqdm


def itags(yt, resolution='1080p', with_video=True):
    max_audio = 0
    audio_value = 0
    for audio_stream in yt.streams.filter(only_audio=True):
        abr = int(audio_stream.abr.replace('kbps', ''))
        if abr > max_audio:
            max_audio = abr
            audio_value = audio_stream.itag
    streams = yt.streams

    if with_video is False:
        return audio_value, None


    try:
        video_tag = streams.filter(res=resolution, fps=60)[0].itag
        print('60 FPS')
    except IndexError:
        video_tag = streams.filter(res=resolution, fps=30)
        if video_tag:
            video_tag = video_tag[0].itag
            print('30 FPS')
        else:
            video_tag = streams.filter(res=resolution, fps=24)[0].itag
            print('24 FPS')
    return audio_value, video_tag


if __name__ == "__main__":
    filename = "src/ytdownloader/conf/playlist/germany_2025.csv"
    df = pd.read_csv(filename)
    outroot = Path("output/germany")
    outroot.mkdir(parents=True, exist_ok=True)

    

    for ir, row in tqdm(df.iterrows(), total=df.shape[0]):
        url = row["URL"].strip()
        title = row["Title"].strip()
        yt = YouTube(url, on_progress_callback=on_progress)

        outfile = f"{title}.m4a"
            
        audio, video = itags(yt=yt, resolution='1080p', with_video=False) # specify the resolution    
        yt.streams.get_by_itag(audio).download(output_path=outroot, filename=outfile) # downloads audio
        if video:
            yt.streams.get_by_itag(video).download() # downloads video