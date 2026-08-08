#!/bin/sh

set -u

OPTIONS="/data/options.json"
PYFILE="/data/reolink_media_test.py"

UID_VALUE="$(jq -r '.uid' "$OPTIONS")"
USERNAME_VALUE="$(jq -r '.username' "$OPTIONS")"
PASSWORD_VALUE="$(jq -r '.password' "$OPTIONS")"

echo "========================================"
echo " REOLINK P2P MEDIA TEST"
echo "========================================"

cat > "$PYFILE" <<PYTHON
import traceback
import inspect
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

    print("RESULT: CAMERA_METHODEN", flush=True)

    for name in dir(camera):
        if not name.startswith("_"):
            try:
                obj = getattr(camera, name)

                if callable(obj):
                    try:
                        sig = inspect.signature(obj)
                    except Exception:
                        sig = "?"

                    print(
                        "RESULT: METHOD="
                        + name
                        + " "
                        + str(sig),
                        flush=True
                    )
            except Exception:
                pass

    print("RESULT: CONNECT_START", flush=True)

    camera.connect()

    print("RESULT: CONNECT_OK", flush=True)

    print("RESULT: SUCHE_STREAM_METHODEN", flush=True)

    stream_names = [
        name for name in dir(camera)
        if (
            "stream" in name.lower()
            or "media" in name.lower()
            or "read" in name.lower()
            or "recv" in name.lower()
        )
    ]

    for name in stream_names:
        print(
            "RESULT: STREAM_OBJECT="
            + name,
            flush=True
        )

    print("RESULT: TEST_30_SEKUNDEN", flush=True)

    start = time.time()

    while time.time() - start < 30:
        print(
            "RESULT: WARTEN "
            + str(round(time.time() - start, 1))
            + "s",
            flush=True
        )
        time.sleep(5)

    print("RESULT: TEST_ENDE", flush=True)

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

echo "RESULT: PYTHON_EXITCODE=$RC"
echo "RESULT: SHELL_ENDE"

exit "$RC"
