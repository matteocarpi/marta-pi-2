#!/usr/bin/env python3
import os
import subprocess
import time

import media

AUDIO_DEVICE = os.environ.get("AUDIO_DEVICE", "plughw:Headphones")
AUDIO_VOLUME = os.environ.get("AUDIO_VOLUME", "100%")
RETRY_SECONDS = 5


def set_volume():
    card = AUDIO_DEVICE.split(":", 1)[-1].split(",", 1)[0]
    result = subprocess.run(
        ["amixer", "-q", "-c", card, "sset", "PCM", AUDIO_VOLUME, "unmute"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"Could not set volume on {card}: {result.stderr.strip()}", flush=True)


def main():
    set_volume()
    playing = None
    while True:
        path = media.audio()
        if path is None:
            print("No audio found, waiting...", flush=True)
            time.sleep(RETRY_SECONDS)
            continue
        if path != playing:
            print(f"Playing {path}", flush=True)
            playing = path
        result = subprocess.run(["mpg123", "-q", "-o", "alsa", "-a", AUDIO_DEVICE, str(path)])
        if result.returncode != 0:
            print(f"mpg123 exited with code {result.returncode}", flush=True)
            time.sleep(RETRY_SECONDS)


if __name__ == "__main__":
    main()
