#!/usr/bin/env python3
import os
import subprocess
import time
from pathlib import Path

AUDIO_FILE = Path(
    os.environ.get("AUDIO_FILE", Path(__file__).resolve().parent / "audio" / "audio.mp3")
)
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
    while True:
        if not AUDIO_FILE.is_file():
            print(f"Audio file not found: {AUDIO_FILE}, waiting...", flush=True)
            time.sleep(RETRY_SECONDS)
            continue
        result = subprocess.run(["mpg123", "-q", "-o", "alsa", "-a", AUDIO_DEVICE, str(AUDIO_FILE)])
        if result.returncode != 0:
            print(f"mpg123 exited with code {result.returncode}", flush=True)
            time.sleep(RETRY_SECONDS)


if __name__ == "__main__":
    main()
