#!/usr/bin/env python3
import threading

import audio
import slideshow


def main():
    threading.Thread(target=audio.main, daemon=True).start()
    slideshow.main()


if __name__ == "__main__":
    main()
