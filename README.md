# obs-keyboard
Python test to control OBS using an USB Keypad under Ubuntu.

(Has been tested with an old "HEDEN" USB keypad model "PAV2USB190" under Ubuntu 18.04.4 LTS)

_Licensed under the MIT License_

## Usage

Update the first line 90-extra-keyboard.hwdb with your pid and vid (from lsusb).

```
sudo ./setup.sh
sudo pip3 install -r requirements.txt
sudo ./obs-keyboard.py
```
