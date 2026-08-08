#!/bin/sh

echo "========================================"
echo " REOLINK P2P RAW UDP STREAM TEST"
echo "========================================"

UID="$(python3 -c '
import json
with open("/data/options.json") as f:
    d=json.load(f)
print(d.get("uid",""))
')"

USERNAME="$(python3 -c '
import json
with open("/data/options.json") as f:
    d=json.load(f)
print(d.get("username","admin"))
')"

PASSWORD="$(python3 -c '
import json
with open("/data/options.json") as f:
    d=json.load(f)
print(d.get("password",""))
')"

export REOLINK_UID="$UID"
export REOLINK_USERNAME="$USERNAME"
export REOLINK_PASSWORD="$PASSWORD"

echo "RESULT: OPTIONS_GELESEN"
echo "RESULT: UID=$UID"
echo "RESULT: USERNAME=$USERNAME"
echo "RESULT: PASSWORD_GESETZT=$( [ -n "$PASSWORD" ] && echo JA || echo NEIN )"
echo "RESULT: PASSWORD_LAENGE=${#PASSWORD}"

cat > /data/reolink_raw_udp_test.py <<'PYTHON'
import os
import time
import binascii

from pyneolink.camera import Camera

UID = os.environ["REOLINK_UID"]
USERNAME = os.environ["REOLINK_USERNAME"]
PASSWORD = os.environ["REOLINK_PASSWORD"]

OUT = "/data/reolink_raw_stream.bin"

print("RESULT: PYTHON_START")

camera = Camera(
    uid=UID,
    username=USERNAME,
    password=PASSWORD,
    discovery="relay",
    stream="both",
    debug=True,
)

print("RESULT: CAMERA_ERZEUGT")

try:
    print("RESULT: CONNECT_START")
    camera.connect()
    print("RESULT: CONNECT_OK")

    print("RESULT: LOGIN_START")
    camera.login()
    print("RESULT: LOGIN_OK")

    print("RESULT: START_STREAM")
    camera.start_stream("mainStream")
    print("RESULT: START_STREAM_OK")

    sock = getattr(camera, "sock", None)

    print(f"RESULT: SOCKET_TYPE={type(sock)}")

    if sock is None:
        print("RESULT: SOCKET_FEHLT")
        raise RuntimeError("Camera socket not available")

    print("RESULT: SOCKET_ATTRS")
    print([
        x for x in dir(sock)
        if not x.startswith("__")
    ])

    print("RESULT: RAW_SOCKET_TEST")

    # Wir benutzen bewusst NICHT camera._recv(),
    # damit PyNeolink die Videodaten nicht als Baichuan
    # Nachricht interpretiert.

    received = 0
    total = 0

    with open(OUT, "wb") as f:

        for i in range(30):

            try:
                data = sock.recv(65535)

                received += 1
                total += len(data)

                print(
                    f"RESULT: UDP_PACKET={received} "
                    f"LEN={len(data)} "
                    f"TOTAL={total}"
                )

                print(
                    "RESULT: FIRST_BYTES="
                    + binascii.hexlify(data[:64]).decode()
                )

                # Suche nach H264 Startcodes
                if b"\x00\x00\x00\x01" in data:
                    print("RESULT: H264_4BYTE_STARTCODE=JA")

                if b"\x00\x00\x01" in data:
                    print("RESULT: H264_3BYTE_STARTCODE=JA")

                if b"H264" in data:
                    print("RESULT: H264_TEXT_MARKER=JA")

                f.write(data)
                f.flush()

            except Exception as e:
                print(
                    f"RESULT: UDP_ERROR="
                    f"{type(e).__name__}: {e}"
                )
                break

    print(f"RESULT: PACKETS={received}")
    print(f"RESULT: BYTES={total}")

finally:

    print("RESULT: STOP_STREAM")

    try:
        camera.stop_stream("mainStream")
        print("RESULT: STOP_STREAM_OK")
    except Exception as e:
        print(
            f"RESULT: STOP_STREAM_FEHLER="
            f"{type(e).__name__}: {e}"
        )

    try:
        camera.close()
        print("RESULT: CLOSE_OK")
    except Exception as e:
        print(
            f"RESULT: CLOSE_FEHLER="
            f"{type(e).__name__}: {e}"
        )

print("RESULT: FILE_CHECK")

try:
    size = os.path.getsize(OUT)
    print(f"RESULT: FILE_SIZE={size}")
except Exception as e:
    print(f"RESULT: FILE_ERROR={type(e).__name__}: {e}")

print("RESULT: TEST_ENDE")
PYTHON

echo "RESULT: PYTHON_DATEI_ERSTELLT"
echo "RESULT: STARTE_PYTHON"

python3 /data/reolink_raw_udp_test.py

EXITCODE=$?

echo "RESULT: PYTHON_EXITCODE=$EXITCODE"
echo "RESULT: SHELL_ENDE"
