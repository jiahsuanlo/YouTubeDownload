# YouTubeDownload
An app to download YouTube videos

# Installation
1. Clone the code
    ```
    git clone https://github.com/jiahsuanlo/YouTubeDownload.git
    ```
2. At the main directory, set up virtual environment
   ```
   cd YouTubeDownload
   python3 -m venv .venv
   ```
3. Activate the environment
   ```
   source activate.sh
   ```
4. Install the module
   ```
   pip install .
   ```

# To Use
Add a new video/song list yaml file in the `conf/playlist` directory. There are some existing sample yaml files in that directory for the reference.

Then re-install the module again after your yaml file is added
```
pip install .
```
Run the script to download the files now
```
ytdownload playlist=<your-playlist.yaml>
```

The download video/audio files will be saved in `output` directory