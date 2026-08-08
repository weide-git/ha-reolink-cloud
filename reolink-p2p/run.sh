#!/bin/sh

set -u

OPTIONS="/data/options.json"
PYFILE="/data/reolink_connect_test.py"

UID_VALUE="$(jq -r '.uid' "$OPTIONS")"
USERNAME_VALUE="$(jq -r '.username' "$OPTIONS")"
PASSWORD_VALUE="$(jq -r '.password' "$OPTIONS")"

echo "========================================"
echo " REOLINK P2P CONNECT TEST"
echo "========================================"

cat > "$PYFILE" <<PYTHON
import traceback
import time

print("RESULT: PYTHON_START", flush=True)

try:
    import pyneolink

    print(
        "RESULT: PYNEOLINK_VERSION="
        + str(getattr(pyneolink, "__version__", "unknown")),
        flush=True
    )

    from pyneolink.camera import Camera

    print("RESULT: CAMERA_IMPORT_OK", flush=True)

    camera = Camera(
        uid="${UID_VALUE}",
        username="${USERNAME_VALUE}",
        password="${PASSWORD_VALUE}",
        discovery="relay",
        stream="subStream",
        timeout=30.0,
        debug=True,
    )

    print("RESULT: CAMERA_ERZEUGT", flush=True)
    print("RESULT: STARTE_CONNECT", flush=True)

    if not hasattr(camera, "connect"):
        print("RESULT: KEIN_CONNECT_METHOD", flush=True)
    else:
        print("RESULT: CONNECT_METHOD_VORHANDEN", flush=True)

        try:
            result = camera.connect()

            print(
                "RESULT: CONNECT_ERGEBNIS="
                + repr(result),
                flush=True
            )

            print("RESULT: CONNECT_ERFOLGREICH", flush=True)

        except BaseException as e:
            print(
                "RESULT: CONNECT_FEHLER="
                + repr(e),
                flush=True
            )

            traceback.print_exc()

    print("RESULT: TEST_ENDE", flush=True)

except BaseException as e:
    print(
        "RESULT: HAUPTFEHLER="
        + repr(e),
        flush=True
    )

    traceback.print_exc()

print("RESULT: PYTHON_ENDE", flush=True)
PYTHON

echo "RESULT: PYTHON_DATEI_ERSTELLT"
echo "RESULT: STARTE_PYTHON"

python -u "$PYFILE"

RC="$?"

echo "RESULT: PYTHON_EXITCODE=$RC"
echo "RESULT: SHELL_ENDE"

exit "$RC"
