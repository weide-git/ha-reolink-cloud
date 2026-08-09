```sh
#!/bin/sh

echo "========================================"
echo "REOLINK P2P RAW UDP TRANSPORT TEST"
echo "========================================"

echo "RESULT: SHELL_START"

if [ -f /data/options.json ]; then
    echo "RESULT: OPTIONS_VORHANDEN"
else
    echo "RESULT: OPTIONS_VORHANDEN=NEIN"
fi

if [ -f /data/reolink_raw_udp_test.py ]; then
    echo "RESULT: PYTHON_DATEI_VORHANDEN=JA"
else
    echo "RESULT: PYTHON_DATEI_VORHANDEN=NEIN"
    echo "ERROR: /data/reolink_raw_udp_test.py fehlt"
    echo "RESULT: SHELL_ENDE"
    exit 2
fi

echo "RESULT: STARTE_PYTHON"

python3 /data/reolink_raw_udp_test.py
RC=$?

echo "RESULT: PYTHON_EXITCODE=$RC"
echo "RESULT: SHELL_ENDE"

exit "$RC"
```
