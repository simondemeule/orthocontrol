import rtmidi
import time
from Quartz.CoreGraphics import CGEventPost
from Quartz.CoreGraphics import kCGHIDEventTap
from Quartz.CoreGraphics import kCGEventFlagMaskShift
from Quartz.CoreGraphics import kCGEventFlagMaskAlternate
from AppKit import NSEvent
from CoreMIDI import MIDIRestart

# bits taken from:
# https://github.com/boppreh/keyboard/blob/master/keyboard/_darwinkeyboard.py

CODE_VOLUME_UP = 0
CODE_VOLUME_DOWN = 1
CODE_PLAY = 16

FLAG_DEFAULT = 0
FLAG_ALT_SHIFT = kCGEventFlagMaskShift + kCGEventFlagMaskAlternate

def tap(code, flags=0):
    event = NSEvent.otherEventWithType_location_modifierFlags_timestamp_windowNumber_context_subtype_data1_data2_(
        14, # type
        (0, 0), # location
        0xa00 + flags, # flags
        0, # timestamp
        0, # window
        0, # ctx
        8, # subtype
        (code << 16) | (0xa << 8), # data1
        -1 # data2
    )
    CGEventPost(kCGHIDEventTap, event.CGEvent())
    event = NSEvent.otherEventWithType_location_modifierFlags_timestamp_windowNumber_context_subtype_data1_data2_(
        14, # type
        (0, 0), # location
        0xb00 + flags, # flags
        0, # timestamp
        0, # window
        0, # ctx 
        8, # subtype
        (code << 16) | (0xb << 8), # data1
        -1 # data2
    )
    CGEventPost(kCGHIDEventTap, event.CGEvent())

def volume(up, quadruple=False):
    code = CODE_VOLUME_UP if up else CODE_VOLUME_DOWN
    flags = FLAG_DEFAULT if quadruple else FLAG_ALT_SHIFT
    tap(code, flags)

def play():
    tap(CODE_PLAY)

scroll_last = None
# scroll_last_time = None
click_last = 0

def callback(message, delta):
    global scroll_last
    # global scroll_last_time
    global click_last
    if message[0][0] == 176:
        scroll_now = message[0][2]
        # scroll_now_time = time.perf_counter()
        if scroll_now != scroll_last:
            if scroll_now is not None and scroll_last is not None:
                # quadruple = (scroll_now_time - scroll_last_time) < 0.01
                quadruple = False
                volume(scroll_now > scroll_last, quadruple)
                # volume(scroll_now > scroll_last)
            scroll_last = scroll_now
            # scroll_last_time = scroll_now_time
    elif message[0][0] == 144 or message[0][0] == 128:
        click_now = message[0][2] == 100
        if click_now != click_last:
            if click_now:
                play()
            click_last = click_now

port_name = "Ortho Remote Bluetooth"
retry_interval = 5
retry_restart_MIDI = True

midi = rtmidi.MidiIn()

while True:
    ports = midi.get_ports()
    if port_name in ports:
        try:
            with midi.open_port(ports.index(port_name)):
                print(f"Port opened successfully: '{port_name}'")
                midi.set_callback(callback)
                while True:
                    time.sleep(retry_interval)
                    ports = midi.get_ports()
                    if not port_name in ports:
                        break
                midi.cancel_callback()
            print(f"Port closed: '{port_name}'")
        except Exception:
            print(f"Port failed to open or encountered an error: '{port_name}'")
        if retry_restart_MIDI:
            print("Restarting MIDI server")
            MIDIRestart()
    else:
        print(f"Port unavaliable: '{port_name}'")
        print(f"Currently avaliable ports: {ports}")
    time.sleep(retry_interval)
