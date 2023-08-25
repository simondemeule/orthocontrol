import subprocess
import sys
import rtmidi
import time
import getopt
from Quartz.CoreGraphics import CGEventPost
from Quartz.CoreGraphics import kCGHIDEventTap
from Quartz.CoreGraphics import kCGEventFlagMaskShift
from Quartz.CoreGraphics import kCGEventFlagMaskAlternate
from AppKit import NSEvent
from CoreMIDI import MIDIRestart

options, _ = getopt.getopt(sys.argv[1:], [], ["midi-name=", "midi-restart", "midi-restart-interval=", "midi-sysex", "midi-notifications"])
options = dict(options)

if not ("--midi-name" in options):
    print("Missing --midi-name argument")
    sys.exit(1)

port_name = options["--midi-name"]

if "--midi-restart" in options:
    restart_enable = True
else:
    restart_enable = False

if "--midi-restart-interval" in options:
    restart_interval = float(options["--midi-restart-interval"])
else:
    restart_interval = 1.0

if "--midi-sysex" in options:
    sysex_enable = True
else:
    sysex_enable = False

if "--midi-notifications" in options:    
    notification_enable = True
else:
    notification_enable = False

print("Applied arguments:")
print(f"  MIDI port name:        {port_name}'")
print(f"  MIDI restart:          {restart_enable}")
print(f"  MIDI restart interval: {restart_interval}")
print(f"  MIDI sysex:            {sysex_enable}")
print(f"  MIDI notifications:    {notification_enable}")

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
click_last = 0

def callback(message, delta):
    global scroll_last
    global click_last
    if message[0][0] == 176:
        if message[0][2] == 1:
            volume(True)
        elif message[0][2] == 127:
            volume(False)
    elif message[0][0] == 144 or message[0][0] == 128:
        click_now = message[0][2] == 100
        if click_now != click_last:
            if click_now:
                play()
            click_last = click_now

midi_in = rtmidi.MidiIn()
midi_out = rtmidi.MidiOut()

if restart_enable:
    print("Restarting MIDI server")
    MIDIRestart()

notification_command = '''
on run argv
  display notification (item 2 of argv) with title (item 1 of argv)
end run
'''

def notification(notification_message):
    print(notification_message)
    if notification_enable:
        subprocess.call(['osascript', '-e', notification_command, 'OrthoControl', notification_message])

"""
OR1 SYSEX SPEC
strt | TE       OR1 | cmd  addr values | end
-----|--------------|------------------|----
F0   | 00 20 76 02  | xx   xx   xx ... | F7

cmd
00      write
01      read

addr    setting                            default     note
00      midi channel                       0
01      midi cc                            1
02      midi cc abs (0 or 1)               1           set to 1 to enable absolute mode
03      midi note                          60
04      midi velocity                      100
05      disable hid                        0           set to 1 to disable hid - will restart remote
06      set cc absolute value              63          write 63 to reset

values
write   list of values for consecutive addresses after addr
read    number of consecutive addresses to read after addr (0 = read all)
        - response msg can be used to write those values back

EXAMPLES
F0 00 20 76 02 00 01 0e F7     set send cc 14
F0 00 20 76 02 01 00 00 F7     read all
"""

while True:
    ports_in = midi_in.get_ports()
    ports_out = midi_out.get_ports()
    if port_name in ports_in and port_name in ports_out:
        try:
            with midi_in.open_port(ports_in.index(port_name)) as port_in, midi_out.open_port(ports_out.index(port_name)) as port_out:
                notification(f"Port opened successfully: '{port_name}'")
                if sysex_enable:
                    print(f"Sending sysex to enable relative mode")
                    midi_out.send_message([0xF0, 0x00, 0x20, 0x76, 0x02, 0x00, 0x02, 0x00, 0xF7])
                midi_in.set_callback(callback)
                while True:
                    time.sleep(restart_interval)
                    ports_in = midi_in.get_ports()
                    ports_out = midi_out.get_ports()
                    if not port_name in ports_in or not port_name in ports_out:
                        break
                midi_in.cancel_callback()
            notification(f"Port closed: '{port_name}'")
        except Exception:
            notification(f"Port failed to open or encountered an error: '{port_name}'")         
    else:
        notification(f"Port unavaliable: '{port_name}'")
        print(f"Currently avaliable ports (in):  {ports_in}")
        print(f"Currently avaliable ports (out): {ports_out}")
    if restart_enable:
        notification("Restarting MIDI server")
        MIDIRestart()
    time.sleep(restart_interval)
