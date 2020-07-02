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
pages = {}
scenes = ws.call(requests.GetSceneList())
current_page = 1
max_pages = 1

for s in scenes.getScenes():
    if not ":" in s['name']:
        continue
    i = s['name'].split(":")[0]
    if not i.isnumeric():
        continue
    i = int(i)
    if i>=10:
        p = i//10
        i = i%10
        if not p in pages:
            pages[p] = {}
        if p>max_pages:
            max_pages=p
        pages[p]["KEY_NUMERIC_%d" % (i)] = requests.SetPreviewScene(s['name'])
    else:
        keys["KEY_NUMERIC_%d" % (i)] = requests.SetPreviewScene(s['name'])

if not keys:
    print("No prefixes in scenes, fallback to scenes order.")
    next_key = 0
    for s in scenes.getScenes():
        p = next_key//10
        i = next_key%10
        if not p in pages:
            pages[p] = {}
        if p>max_pages:
            max_pages=p
        pages[p]["KEY_NUMERIC_%d" % (i)] = requests.SetPreviewScene(s['name'])
        next_key += 1

print("Got %d pages."%(max_pages))

#keys["KEY_NUMERIC_A"] = None
keys["KEY_NUMERIC_B"] = requests.TransitionToProgram({'name': 'Fondu'})
keys["KEY_NUMERIC_C"] = requests.TransitionToProgram({'name': 'Stinger'})
keys["KEY_NUMERIC_D"] = requests.TransitionToProgram({'name': 'Coupure'})

#keys["KEY_NUMERIC_STAR"] = None
#keys["KEY_NUMERIC_POUND"] = None

print("==========")
print("* DEFAULT *")
for k in keys:
    print("%s => %s" % (k, keys[k]))
for p in pages:
    print("* PAGE %d *"%(p))
    for k in pages[p]:
        print("%s => %s" % (k, pages[p][k]))
print("==========")

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
        if keyevent.keycode == "KEY_F24":
            current_page+=1
            if current_page > max_pages:
                current_page=1
            print("Page: %d"%(current_page))
            continue
        if keyevent.keycode in keys:
            ws.call(keys[keyevent.keycode])
        if keyevent.keycode in pages[current_page]:
            ws.call(pages[current_page][keyevent.keycode])
    except Exception as ex:
        logger.exception("Fail!")

ws.disconnect()
