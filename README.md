# Martapi

Shows an image on the Raspberry Pi's LCD and plays an audio file on a loop. It starts automatically when the Pi boots.

## Install on a new Pi

1. Flash Raspberry Pi OS onto the SD card with Raspberry Pi Imager. Set the user to `admin` and enable SSH.
2. Install the LCD driver, if the screen doesn't work yet (this reboots the Pi):
   ```bash
   git clone https://github.com/goodtft/LCD-show.git
   cd LCD-show && chmod +x LCD35-show && sudo ./LCD35-show
   ```
3. Connect to the Pi and install Martapi:
   ```bash
   git clone https://github.com/matteocarpi/marta-pi-2.git
   cd marta-pi-2
   ./install.sh
   ```
4. Plug a speaker into the 3.5mm headphone jack.

The image appears on the screen and the audio starts playing.

## Media

By default the Pi uses the media in this repo:

- `images/`: the first image, in alphabetical order, is shown
- `audio/`: the first `.mp3`, in alphabetical order, is played

To give a Pi its own media without changing the repo:

1. Turn off the Pi and put its SD card in your computer.
2. Open the `bootfs` drive and go to the `martapi` folder.
3. Put your image in `martapi/images/` and your `.mp3` in `martapi/audio/`.
4. Put the card back in the Pi and turn it on.

You can replace only the image, only the audio, or both. Anything you don't replace comes from the repo.

## Set up many Pis by copying the SD card

1. Install one Pi as described above and check that it works.
2. Prepare it for copying:
   ```bash
   sudo rm -f /boot/firmware/martapi/images/* /boot/firmware/martapi/audio/*
   sudo truncate -s 0 /etc/machine-id
   sudo rm -f /etc/ssh/ssh_host_*
   sudo systemctl enable regenerate_ssh_host_keys
   sudo poweroff
   ```
3. Put the SD card in your Mac and create an image of it. Replace `disk4` with your card's disk number from `diskutil list`:
   ```bash
   diskutil unmountDisk /dev/disk4
   sudo dd if=/dev/rdisk4 of=~/martapi.img bs=4m status=progress
   ```
4. Flash `martapi.img` onto each new card with Raspberry Pi Imager: **Choose OS → Use custom**. Skip the OS customisation step.
5. Add each Pi's media to `bootfs/martapi/` as described above.
6. After the first boot, give each Pi its own name:
   ```bash
   sudo hostnamectl set-hostname martapi-3
   ```

## Update

```bash
cd ~/marta-pi-2
git pull
./install.sh
```

## Settings

To change these on one Pi, create `/etc/martapi.env`, for example:

```
AUDIO_VOLUME=80%
```

| Setting        | Default             | What it does                         |
| -------------- | ------------------- | ------------------------------------ |
| `AUDIO_VOLUME` | `100%`              | Speaker volume                       |
| `AUDIO_DEVICE` | `plughw:Headphones` | Audio output (`plughw:b1` for HDMI)  |
| `FB_DEVICE`    | `/dev/fb1`          | Screen to draw on                    |

Then run `sudo systemctl restart martapi`.

## Troubleshooting

```bash
sudo systemctl status martapi        # is it running?
journalctl -u martapi -n 30          # logs: shows which image and audio are used
```
