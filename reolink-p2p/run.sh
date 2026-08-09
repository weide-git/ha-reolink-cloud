#!/bin/sh
set +e

echo "========================================"
echo " REOLINK P2P RAW UDP TRANSPORT TEST"
echo "========================================"
echo "RESULT: SHELL_START"

if [ ! -f /data/options.json ]; then
    echo "RESULT: OPTIONS_FEHLEN"
    exit 1
fi

echo "RESULT: OPTIONS_VORHANDEN"
echo "RESULT: PYTHON_DATEI_VORHANDEN=$(test -f /data/reolink_raw_udp_test.py && echo JA || echo NEIN)"

python3 /data/reolink_raw_udp_test.py
RC=$?

echo "RESULT: PYTHON_EXITCODE=$RC"
echo "RESULT: SHELL_ENDE"
exit 0
