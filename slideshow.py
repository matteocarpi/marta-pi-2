#!/usr/bin/env python3
import os
import time
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps

IMAGES_DIR = Path(os.environ.get("SLIDESHOW_DIR", "/home/admin/images"))
FB_DEVICE = os.environ.get("FB_DEVICE", "/dev/fb0")
SLIDE_SECONDS = float(os.environ.get("SLIDE_SECONDS", "10"))
TTY = os.environ.get("SLIDESHOW_TTY", "/dev/tty1")
EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp"}


def read_sysfs(name):
    fb = Path(FB_DEVICE).name
    return Path(f"/sys/class/graphics/{fb}/{name}").read_text().strip()


def framebuffer_info():
    width, height = (int(v) for v in read_sysfs("virtual_size").split(","))
    bpp = int(read_sysfs("bits_per_pixel"))
    stride = int(read_sysfs("stride"))
    return width, height, bpp, stride


def prepare_console():
    # Hide the blinking cursor and disable console blanking so the screen stays on.
    try:
        Path("/sys/class/graphics/fbcon/cursor_blink").write_text("0")
    except OSError:
        pass
    try:
        with open(TTY, "w") as tty:
            tty.write("\033[?25l\033[9;0]\033[2J")
    except OSError:
        pass


def to_framebuffer_bytes(img, width, height, bpp, stride):
    rgb = np.asarray(img.convert("RGB"), dtype=np.uint8)
    if bpp == 32:
        pixels = np.empty((height, width, 4), dtype=np.uint8)
        pixels[..., 0] = rgb[..., 2]
        pixels[..., 1] = rgb[..., 1]
        pixels[..., 2] = rgb[..., 0]
        pixels[..., 3] = 255
        rows = pixels.reshape(height, width * 4)
    elif bpp == 16:
        r = rgb[..., 0].astype(np.uint16)
        g = rgb[..., 1].astype(np.uint16)
        b = rgb[..., 2].astype(np.uint16)
        rgb565 = ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3)
        rows = rgb565.astype("<u2").view(np.uint8).reshape(height, width * 2)
    else:
        raise RuntimeError(f"Unsupported framebuffer depth: {bpp} bpp")

    if rows.shape[1] < stride:
        padded = np.zeros((height, stride), dtype=np.uint8)
        padded[:, : rows.shape[1]] = rows
        rows = padded
    return rows.tobytes()


def fit_to_screen(path, width, height):
    with Image.open(path) as img:
        img = ImageOps.exif_transpose(img)
        img = ImageOps.contain(img.convert("RGB"), (width, height))
    canvas = Image.new("RGB", (width, height), "black")
    canvas.paste(img, ((width - img.width) // 2, (height - img.height) // 2))
    return canvas


def list_images():
    if not IMAGES_DIR.is_dir():
        return []
    return sorted(
        p for p in IMAGES_DIR.iterdir() if p.is_file() and p.suffix.lower() in EXTENSIONS
    )


def main():
    width, height, bpp, stride = framebuffer_info()
    print(f"Framebuffer {FB_DEVICE}: {width}x{height} {bpp}bpp, stride {stride}", flush=True)
    prepare_console()

    with open(FB_DEVICE, "r+b", buffering=0) as fb:
        while True:
            images = list_images()
            if not images:
                print(f"No images in {IMAGES_DIR}, waiting...", flush=True)
                time.sleep(SLIDE_SECONDS)
                continue

            path = images[0]
            try:
                frame = fit_to_screen(path, width, height)
            except Exception as exc:
                print(f"Cannot show {path.name}: {exc}", flush=True)
                time.sleep(SLIDE_SECONDS)
                continue
            fb.seek(0)
            fb.write(to_framebuffer_bytes(frame, width, height, bpp, stride))
            time.sleep(SLIDE_SECONDS)


if __name__ == "__main__":
    main()
