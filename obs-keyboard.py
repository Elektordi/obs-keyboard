#!/usr/bin/env python3

import sys
from evdev import InputDevice, categorize, ecodes
from obswebsocket import obsws, requests

if len(sys.argv)<2:
    print("Usage: sudo %s /dev/input/eventXX" % (sys.argv[0]))
    sys.exit(1)

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(sys.argv[0])

host = "localhost"
port = 4444
password = "secret"

ws = obsws(host, port, password)
ws.connect()

keys = {}
next_key = 0
scenes = ws.call(requests.GetSceneList())
for s in scenes.getScenes()[:10]:
    keys["KEY_NUMERIC_%d" % (next_key)] = requests.SetPreviewScene(s['name'])
    next_key += 1

#keys["KEY_NUMERIC_A"] = None
keys["KEY_NUMERIC_B"] = requests.TransitionToProgram({'name': 'Fondu'})
keys["KEY_NUMERIC_C"] = requests.TransitionToProgram({'name': 'Stinger'})
keys["KEY_NUMERIC_D"] = requests.TransitionToProgram({'name': 'Coupure'})

#keys["KEY_NUMERIC_STAR"] = None
#keys["KEY_NUMERIC_POUND"] = None

for k in keys:
    print("%s => %s" % (k, keys[k]))

dev = InputDevice(sys.argv[1])
logger.info(dev)

for event in dev.read_loop():
    try:
        if event.type != ecodes.EV_KEY:
            continue
        keyevent = categorize(event)
        if keyevent.keystate != 1: # down
            continue
        logger.info(keyevent.keycode)
        if keyevent.keycode in keys:
            ws.call(keys[keyevent.keycode])
    except Exception as ex:
        logger.exception("Fail!")

ws.disconnect()
