#!/usr/bin/env bash
set -euo pipefail

if [[ $EUID -ne 0 ]]; then
    exec sudo "$0" "$@"
fi

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BOOT_DIR=/boot/firmware
[[ -d $BOOT_DIR ]] || BOOT_DIR=/boot

apt-get update
apt-get install -y python3-numpy python3-pil mpg123 alsa-utils

mkdir -p "$BOOT_DIR/martapi/images" "$BOOT_DIR/martapi/audio"

sed "s|@REPO_DIR@|$REPO_DIR|g" "$REPO_DIR/martapi.service" > /etc/systemd/system/martapi.service
systemctl daemon-reload
systemctl enable martapi
systemctl restart martapi

echo "Martapi installed from $REPO_DIR"
echo "Override media by copying files into $BOOT_DIR/martapi/images and $BOOT_DIR/martapi/audio"
