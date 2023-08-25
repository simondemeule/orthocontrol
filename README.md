# macOS volume control through Teenage Engineering Ortho Remote

Adjusts volume in fine 1/64 increments by emulating alt + shift + volume up / down. Much smoother than setting the volume through AppleScript, or through the default 1/16 increment behaviour. Also allows play / pause by clicking.

# How to use

Install by running `sh setup.sh`. Activate the environment with `source env/bin/activate`. Run with `python3 orthocontrol.py` or `sh run.sh` with your arguments of choice. You might want to run this on system startup if you want this to work whenever your Ortho Remote is connected. 

Here are the arguments:
- `--midi-name` provides the name of the MIDI port of the Ortho Remote. This is required.
- `--midi-restart` will cause a restart of the MIDI server when connection is unsuccessful. This might be necessary to allow the Ortho Remote to reconnect. This can mess with other MIDI devices and MIDI applications.
- `--midi-restart-interval` sets the time between restarts in seconds.
- `--midi-sysex` enables a MIDI SYSEX message that sets the Ortho Remote in relative position mode. This prevents reaching a dead zone at the extremes of the CC ranges.
- `--midi-notifications` enables notifications sent through osascript that provide information on the connection status. This can be useful to know when Ortho Remote goes to sleep so you can nudge it back awake, or kill the script if you are away from Ortho Remote.

Feel free to strip out the Ortho Remote specific logic and integrate this with whatever encoder controller you have!
