#!/bin/sh

echo "# REOLINK P2P RAW UDP TRANSPORT TEST"
echo "RESULT: SHELL_START"
echo "RESULT: CURRENT_DIR=$(pwd)"

echo "RESULT: PYTHON_DATEI_IM_IMAGE:"
ls -l /app/reolink_raw_udp_test.py

echo "RESULT: OPTIONS_VORHANDEN"

if [ -f /data/options.json ]; then
    echo "JA"
else
    echo "NEIN"
    echo "RESULT: SHELL_ENDE"
    exit 1
fi

echo "RESULT: PYTHON_START"

exec python3 -u /app/reolink_raw_udp_test.py
