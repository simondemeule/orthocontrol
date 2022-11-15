PATHPROJECT=$(dirname "$0")
. $PATHPROJECT"/env/bin/activate"
python3 $PATHPROJECT"/orthocontrol.py" --midi-name="Ortho Remote Bluetooth" --midi-restart --midi-retry-interval=1 