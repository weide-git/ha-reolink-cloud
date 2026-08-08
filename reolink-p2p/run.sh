#!/bin/sh

set -u

OPTIONS="/data/options.json"
PYFILE="/data/reolink_stream_test.py"

UID_VALUE="$(jq -r '.uid' "$OPTIONS")"
USERNAME_VALUE="$(jq -r '.username' "$OPTIONS")"
PASSWORD_VALUE="$(jq -r '.password' "$OPTIONS")"

echo "========================================"
echo " REOLINK P2P DIRECT STREAM TEST"
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
        stream="mainStream",
        timeout=30.0,
        debug=True,
    )

    print("RESULT: CAMERA_ERZEUGT", flush=True)

    print("RESULT: CONNECT_START", flush=True)

    camera.connect()

    print("RESULT: CONNECT_OK", flush=True)

    print("RESULT: START_STREAM", flush=True)

    camera.start_stream("mainStream")

    print("RESULT: START_STREAM_OK", flush=True)

    print("RESULT: READ_STREAM_START", flush=True)

    payloads = camera.read_stream_payloads("mainStream")

    start = time.time()
    count = 0
    total_bytes = 0

    for payload in payloads:

        count += 1

        try:
            size = len(payload)
        except Exception:
            size = -1

        total_bytes += max(size, 0)

        print(
            "RESULT: PAYLOAD="
            + str(count)
            + " BYTES="
            + str(size)
            + " TOTAL="
            + str(total_bytes),
            flush=True
        )

        if count >= 10:
            print("RESULT: 10_PAYLOADS_ERHALTEN", flush=True)
            break

        if time.time() - start > 30:
            print("RESULT: STREAM_TIMEOUT_30S", flush=True)
            break

    print(
        "RESULT: PAYLOAD_COUNT="
        + str(count),
        flush=True
    )

    print(
        "RESULT: TOTAL_BYTES="
        + str(total_bytes),
        flush=True
    )

    print("RESULT: STOP_STREAM", flush=True)

    try:
        camera.stop_stream("mainStream")
        print("RESULT: STOP_STREAM_OK", flush=True)
    except Exception as e:
        print(
            "RESULT: STOP_STREAM_FEHLER="
            + repr(e),
            flush=True
        )

    try:
        camera.close()
        print("RESULT: CAMERA_CLOSE_OK", flush=True)
    except Exception as e:
        print(
            "RESULT: CAMERA_CLOSE_FEHLER="
            + repr(e),
            flush=True
        )

except BaseException as e:

    print(
        "RESULT: STREAM_FEHLER="
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
