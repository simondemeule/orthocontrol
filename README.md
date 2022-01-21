# macOS volume control through Teenage Engineering Ortho Remote

Adjusts volume in fine 1/64 increments by emulating alt + shift + volume up / down. Much smoother than setting the volume through AppleScript, or through the default 1/16 increment behaviour. Also allows play / pause by clicking.

# How to use

- Set `port_name` to the name of your Ortho Remote.
- Set `retry_interval` to set the time interval (in seconds) between retries.
- Set `retry_restart_MIDI` to request a MIDI server restart whenever the connection is lost. This might be necessary to allow the Ortho Remote to reconnect.

