import time
import os
from player import play

WELCOME = "/home/pi/alice/media/audio/welcome.wav"

# Laisse le système audio se stabiliser
time.sleep(2)

if os.path.exists(WELCOME):
    play(WELCOME)
