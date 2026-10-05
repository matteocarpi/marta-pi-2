#!/usr/bin/env python3
import os
import subprocess
import time
from pathlib import Path

AUDIO_FILE = Path(
    os.environ.get("AUDIO_FILE", Path(__file__).resolve().parent / "audio" / "audio.mp3")
)
RETRY_SECONDS = 5


def main():
    while True:
        if not AUDIO_FILE.is_file():
            print(f"Audio file not found: {AUDIO_FILE}, waiting...", flush=True)
            time.sleep(RETRY_SECONDS)
            continue
        result = subprocess.run(["mpg123", "-q", str(AUDIO_FILE)])
        if result.returncode != 0:
            print(f"mpg123 exited with code {result.returncode}", flush=True)
            time.sleep(RETRY_SECONDS)


if __name__ == "__main__":
    main()
