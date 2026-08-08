#!/bin/sh

set -u

OPTIONS="/data/options.json"
PYFILE="/data/reolink_test.py"

UID_VALUE="$(jq -r '.uid' "$OPTIONS")"
USERNAME_VALUE="$(jq -r '.username' "$OPTIONS")"
PASSWORD_VALUE="$(jq -r '.password' "$OPTIONS")"

echo "========================================"
echo " REOLINK CAMERA CONNECTION TEST"
echo "========================================"

cat > "$PYFILE" <<PYTHON
import traceback

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

    uid = "${UID_VALUE}"
    username = "${USERNAME_VALUE}"
    password = "${PASSWORD_VALUE}"

    print("RESULT: ERZEUGE_CAMERA", flush=True)

    camera = Camera(
        uid=uid,
        username=username,
        password=password,
        discovery="relay",
        stream="subStream",
        timeout=30.0,
        debug=True,
    )

    print("RESULT: CAMERA_ERZEUGT", flush=True)

    print(
        "RESULT: CAMERA_TYP="
        + str(type(camera)),
        flush=True
    )

    print("RESULT: TEST_OBJEKT_ERFOLGREICH", flush=True)

except BaseException as e:
    print(
        "RESULT: FEHLER="
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

echo
echo "RESULT: PYTHON_EXITCODE=$RC"
echo "RESULT: SHELL_ENDE"

exit "$RC"
