#!/bin/sh

echo "========================================"
echo " REOLINK P2P RAW UDP TRANSPORT TEST"
echo "========================================"

echo "RESULT: SHELL_START"

if [ ! -f /data/options.json ]; then
    echo "RESULT: OPTIONS_FEHLEN"
    exit 1
fi

echo "RESULT: OPTIONS_VORHANDEN"

python3 /data/reolink_raw_udp_test.py

EXITCODE=$?

echo "RESULT: PYTHON_EXITCODE=$EXITCODE"
echo "RESULT: SHELL_ENDE"

exit $EXITCODE
