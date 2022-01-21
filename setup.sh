python3 -m venv env
source env/bin/activate
pip3 install pyobjc python-rtmidi 
# needed because of a temporary issue with the CoreMIDI wrapper: https://github.com/ronaldoussoren/pyobjc/issues/425
pip3 uninstall pyobjc-framework-CoreMIDI
pip3 install --no-binary ':all:' pyobjc-framework-CoreMIDI