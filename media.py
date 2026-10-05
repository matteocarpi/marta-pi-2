import os
from pathlib import Path

REPO_DIR = Path(__file__).resolve().parent
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp"}
AUDIO_EXTENSIONS = {".mp3"}


def media_dirs():
    dirs = []
    if override := os.environ.get("MARTAPI_MEDIA_DIR"):
        dirs.append(Path(override))
    dirs += [Path("/boot/firmware/martapi"), Path("/boot/martapi"), REPO_DIR]
    return dirs


def _first_file(subdir, extensions):
    for base in media_dirs():
        folder = base / subdir
        if not folder.is_dir():
            continue
        # Skip dotfiles: macOS writes "._name" metadata files when copying to FAT.
        files = sorted(
            p
            for p in folder.iterdir()
            if p.is_file() and not p.name.startswith(".") and p.suffix.lower() in extensions
        )
        if files:
            return files[0]
    return None


def image():
    return _first_file("images", IMAGE_EXTENSIONS)


def audio():
    return _first_file("audio", AUDIO_EXTENSIONS)
