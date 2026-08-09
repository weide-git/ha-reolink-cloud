#!/bin/bash

echo "# REOLINK P2P RAW UDP TRANSPORT TEST"
echo "RESULT: SHELL_START"
echo "RESULT: CURRENT_DIR=$(pwd)"
echo "RESULT: DATA_INHALT:"
ls -la /data

echo "RESULT: PYTHON_DATEI_IM_IMAGE:"
ls -la /app/reolink_raw_udp_test.py

echo "RESULT: OPTIONS_VORHANDEN"
if [ -f /data/options.json ]; then
    echo "JA"
else
    echo "NEIN"
    exit 1
fi

echo "RESULT: PYTHON_START"

python3 /app/reolink_raw_udp_test.py

RC=$?

echo "RESULT: PYTHON_EXITCODE=$RC"
echo "RESULT: SHELL_ENDE"

exit $RC
