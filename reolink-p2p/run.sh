#!/bin/sh

echo "========================================"
echo "REOLINK P2P RAW UDP TRANSPORT TEST"
echo "========================================"

echo "RESULT: SHELL_START"
echo "RESULT: CURRENT_DIR=$(pwd)"
echo "RESULT: DATA_INHALT:"

ls -la /data

echo "RESULT: ROOT_INHALT:"
ls -la /

echo "RESULT: OPTIONS_VORHANDEN"

if [ -f /data/options.json ]; then
echo "JA"
else
echo "NEIN"
fi

echo "RESULT: SUCHE_PYTHON_DATEI"

find / -name "reolink_raw_udp_test.py" -type f 2>/dev/null

echo "RESULT: DIREKTER_TEST"

if [ -f /data/reolink_raw_udp_test.py ]; then
echo "RESULT: PYTHON_DATEI_VORHANDEN=JA"
echo "RESULT: PYTHON_DATEI_GROESSE=$(wc -c < /data/reolink_raw_udp_test.py)"
else
echo "RESULT: PYTHON_DATEI_VORHANDEN=NEIN"
fi

echo "RESULT: SHELL_ENDE"

exit 0
