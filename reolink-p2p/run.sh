#!/bin/sh

set -u

OPTIONS="/data/options.json"
PYFILE="/data/reolink_raw_stream_test.py"

UID_VALUE="$(jq -r '.uid' "$OPTIONS")"
USERNAME_VALUE="$(jq -r '.username' "$OPTIONS")"
PASSWORD_VALUE="$(jq -r '.password' "$OPTIONS")"

echo "========================================"
echo " REOLINK P2P RAW STREAM TEST"
echo "========================================"

cat > "$PYFILE" <<PYTHON
import traceback
import time
import inspect
import binascii

print("RESULT: PYTHON_START", flush=True)

try:
    from pyneolink.camera import Camera

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

    camera.connect()

    print("RESULT: CONNECT_OK", flush=True)

    camera.start_stream("mainStream")

    print("RESULT: START_STREAM_OK", flush=True)

    print("RESULT: DIREKTER_RECV_TEST", flush=True)

    print(
        "RESULT: RECV_SIGNATURE="
        + str(inspect.signature(camera._recv)),
        flush=True
    )

    print("RESULT: LESE_ROHDATEN", flush=True)

    for i in range(5):

        print(
            "RESULT: RECV_ATTEMPT="
            + str(i + 1),
            flush=True
        )

        try:

            msg = camera._recv(timeout=3.0)

            print(
                "RESULT: RECV_TYPE="
                + str(type(msg)),
                flush=True
            )

            print(
                "RESULT: RECV_REPR="
                + repr(msg)[:500],
                flush=True
            )

            print(
                "RESULT: RECV_ATTRS="
                + str([
                    x for x in dir(msg)
                    if not x.startswith("_")
                ]),
                flush=True
            )

        except Exception as e:

            print(
                "RESULT: RECV_ERROR="
                + repr(e),
                flush=True
            )

            traceback.print_exc()

            break

    print("RESULT: STOP_STREAM", flush=True)

    try:
        camera.stop_stream("mainStream")
        print("RESULT: STOP_OK", flush=True)
    except Exception as e:
        print(
            "RESULT: STOP_ERROR="
            + repr(e),
            flush=True
        )

    try:
        camera.close()
        print("RESULT: CLOSE_OK", flush=True)
    except Exception as e:
        print(
            "RESULT: CLOSE_ERROR="
            + repr(e),
            flush=True
        )

except BaseException as e:

    print(
        "RESULT: FATAL="
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
