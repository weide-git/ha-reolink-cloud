#!/bin/sh

set -u

OPTIONS="/data/options.json"
LOG="/data/reolink_debug.log"

rm -f "$LOG"

UID_VALUE="$(jq -r '.uid' "$OPTIONS")"
USERNAME_VALUE="$(jq -r '.username' "$OPTIONS")"
PASSWORD_VALUE="$(jq -r '.password' "$OPTIONS")"

echo "========================================"
echo " REOLINK P2P DEBUG"
echo "========================================"
echo
echo "RESULT: UID=${UID_VALUE}"
echo "RESULT: USERNAME=${USERNAME_VALUE}"
echo "RESULT: PYNEOLINK_VERSION=$(python -c 'import pyneolink; print(getattr(pyneolink, "__version__", "unknown"))')"
echo
echo "RESULT: STARTE_PYTHON"
echo

python -u - <<PY 2>&1 | tee "$LOG"
import sys
import traceback
import time
import os

print("PYTHON: gestartet", flush=True)

try:
    import pyneolink
    print(
        "PYTHON: PyNeolink="
        + str(getattr(pyneolink, "__version__", "unknown")),
        flush=True
    )

    from pyneolink.camera import Camera

    print("PYTHON: Camera importiert", flush=True)

    uid = "${UID_VALUE}"
    username = "${USERNAME_VALUE}"
    password = "${PASSWORD_VALUE}"

    print("PYTHON: Erzeuge Camera-Objekt", flush=True)

    camera = Camera(
        uid=uid,
        username=username,
        password=password,
        discovery="relay",
        stream="subStream",
        timeout=30.0,
        debug=True,
    )

    print("PYTHON: Camera-Objekt ERZEUGT", flush=True)

    print("PYTHON: Objekt=", repr(camera), flush=True)

    print("PYTHON: Suche Methoden...", flush=True)

    for name in dir(camera):
        if not name.startswith("_"):
            try:
                attr = getattr(camera, name)
                if callable(attr):
                    print(
                        "PYTHON: METHOD="
                        + name,
                        flush=True
                    )
            except Exception:
                pass

    print("PYTHON: Versuche Verbindung", flush=True)

    try:
        result = camera.connect()
        print(
            "PYTHON: CONNECT_RESULT="
            + repr(result),
            flush=True
        )
    except Exception as e:
        print(
            "PYTHON: CONNECT_FEHLER="
            + repr(e),
            flush=True
        )
        traceback.print_exc()

    print("PYTHON: Test beendet", flush=True)

except BaseException as e:
    print(
        "PYTHON: GLOBALER_FEHLER="
        + repr(e),
        flush=True
    )
    traceback.print_exc()

print("PYTHON: ENDE", flush=True)
PY

echo
echo "========================================"
echo " LOGDATEI"
echo "========================================"

if [ -f "$LOG" ]; then
    cat "$LOG"
else
    echo "RESULT: KEINE_LOGDATEI"
fi

echo
echo "========================================"
echo " ENDE"
echo "========================================"
