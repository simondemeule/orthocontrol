# macOS volume control through Teenage Engineering Ortho Remote

Adjusts volume in fine 1/64 increments by emulating alt + shift + volume up / down. Much smoother than setting the volume through AppleScript, or through the default 1/16 increment behaviour. Also allows play / pause by clicking.

# How to use

Install by running `sh setup.sh`. Activate the environment with `source env/bin/activate`. Run with `python3 orthocontrol.py`. You might want to run this on system startup if you want this to work whenever your Ortho Remote is connected.

- Set `port_name` to the name of your Ortho Remote.
- Set `retry_interval` to set the time interval (in seconds) between retries.
- Set `retry_restart_MIDI` to request a MIDI server restart whenever the connection is lost. This might be necessary to allow the Ortho Remote to reconnect. This might also mess with other MIDI devices, I haven't investigated that in depth.

Feel free to strip out the Ortho Remote specific logic and integrate this with whatever encoder controller you have!
