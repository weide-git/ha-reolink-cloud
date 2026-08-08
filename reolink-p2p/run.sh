#!/bin/sh

set -u

OPTIONS="/data/options.json"

UID_VALUE="$(jq -r '.uid' "$OPTIONS")"
USERNAME_VALUE="$(jq -r '.username' "$OPTIONS")"
PASSWORD_VALUE="$(jq -r '.password' "$OPTIONS")"

echo "========================================"
echo " REOLINK CAMERA CONNECTION TEST"
echo "========================================"
echo

echo "RESULT: PYTHON_START"

python -u - <<PY
import sys
import traceback

print("RESULT: PYTHON_OK", flush=True)

try:
    import pyneolink

    print(
        "RESULT: PYNEOLINK_VERSION="
        + str(getattr(pyneolink, "__version__", "unknown")),
        flush=True
    )

    from pyneolink.camera import Camera

    print("RESULT: CAMERA_IMPORT_OK", flush=True)

except Exception as e:
    print("RESULT: IMPORT_ERROR=" + repr(e), flush=True)
    traceback.print_exc()
    sys.exit(1)

print("RESULT: ERZEUGE_CAMERA", flush=True)

try:
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
    print("RESULT: CAMERA_TYP=" + str(type(camera)), flush=True)

except Exception as e:
    print("RESULT: CAMERA_ERZEUGUNG_FEHLER=" + repr(e), flush=True)
    traceback.print_exc()
    sys.exit(2)

print("RESULT: CAMERA_METHODEN", flush=True)

for name in dir(camera):
    if not name.startswith("_"):
        try:
            obj = getattr(camera, name)
            if callable(obj):
                print("RESULT: METHOD=" + name, flush=True)
        except Exception:
            pass

print("RESULT: SUCHE_CONNECT", flush=True)

if hasattr(camera, "connect"):
    print("RESULT: CONNECT_VORHANDEN", flush=True)

    try:
        result = camera.connect()
        print("RESULT: CONNECT_ERGEBNIS=" + repr(result), flush=True)
    except Exception as e:
        print("RESULT: CONNECT_FEHLER=" + repr(e), flush=True)
        traceback.print_exc()

else:
    print("RESULT: CONNECT_NICHT_VORHANDEN", flush=True)

print("RESULT: TEST_ENDE", flush=True)
PY

echo
echo "========================================"
echo " RESULT: SHELL ENDE"
echo "========================================"
