import os

def play(path):
    if path.endswith(".wav"):
        os.system(f"aplay '{path}'")
    elif path.endswith(".mp3"):
        os.system(f"aplay '{path}'")
    elif path.endswith(".mp4"):
        os.system(f"omxplayer '{path}'")
