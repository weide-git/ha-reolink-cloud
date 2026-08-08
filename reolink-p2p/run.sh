#!/bin/sh

echo "========================================"
echo " REOLINK P2P RAW STREAM ANALYSE"
echo "========================================"

PASSWORD="$(python3 -c '
import json
with open("/data/options.json", "r") as f:
    data = json.load(f)
print(data.get("password", ""))
')"

UID="$(python3 -c '
import json
with open("/data/options.json", "r") as f:
    data = json.load(f)
print(data.get("uid", ""))
')"

USERNAME="$(python3 -c '
import json
with open("/data/options.json", "r") as f:
    data = json.load(f)
print(data.get("username", "admin"))
')"

echo "RESULT: OPTIONS_GELESEN"
echo "RESULT: UID=$UID"
echo "RESULT: USERNAME=$USERNAME"
echo "RESULT: PASSWORD_GESETZT=$( [ -n "$PASSWORD" ] && echo JA || echo NEIN )"
echo "RESULT: PASSWORD_LAENGE=${#PASSWORD}"

export REOLINK_UID="$UID"
export REOLINK_USERNAME="$USERNAME"
export REOLINK_PASSWORD="$PASSWORD"

cat > /data/reolink_raw_stream_analyse.py <<'PYTHON'
import os
import time
import pyneolink

from pyneolink.camera import Camera


UID = os.environ["REOLINK_UID"]
USERNAME = os.environ["REOLINK_USERNAME"]
PASSWORD = os.environ["REOLINK_PASSWORD"]

print("RESULT: PYTHON_START")
print(f"RESULT: PYNEOLINK_VERSION={getattr(pyneolink, '__version__', 'unbekannt')}")
print("RESULT: CAMERA_IMPORT_OK")

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
    login_result = camera.login()
    print("RESULT: LOGIN_OK")

    print("RESULT: START_STREAM")
    camera.start_stream("mainStream")
    print("RESULT: START_STREAM_OK")

    print("RESULT: RAW_RECV_START")

    for attempt in range(1, 11):
        print(f"RESULT: RECV_ATTEMPT={attempt}")

        try:
            msg = camera._recv(timeout=3.0)

            print(f"RESULT: RECV_OK={attempt}")
            print(f"RESULT: MSG_TYPE={type(msg)}")

            if hasattr(msg, "header"):
                h = msg.header
                print(f"RESULT: MSG_ID={getattr(h, 'msg_id', None)}")
                print(f"RESULT: MSG_NUM={getattr(h, 'msg_num', None)}")
                print(f"RESULT: BODY_LEN={getattr(h, 'body_len', None)}")
                print(f"RESULT: RESPONSE_CODE={getattr(h, 'response_code', None)}")
                print(f"RESULT: STREAM_TYPE={getattr(h, 'stream_type', None)}")

            payload = getattr(msg, "payload", b"")

            print(f"RESULT: PAYLOAD_TYPE={type(payload)}")
            print(f"RESULT: PAYLOAD_LEN={len(payload)}")

            if payload:
                print(f"RESULT: PAYLOAD_FIRST_32={payload[:32].hex()}")

                # H.264 / Annex-B-Erkennung
                if b"\x00\x00\x00\x01" in payload:
                    print("RESULT: H264_ANNEXB_STARTCODE=JA")

                if b"\x00\x00\x01" in payload:
                    print("RESULT: H264_STARTCODE=JA")

                if b"H264" in payload[:100]:
                    print("RESULT: H264_MARKER=JA")

            print("RESULT: MESSAGE_ANALYSE_ENDE")

        except Exception as e:
            print(
                f"RESULT: RECV_FEHLER={type(e).__name__}: {e}"
            )

        time.sleep(0.2)

    print("RESULT: RAW_RECV_ENDE")

except Exception as e:
    print(f"RESULT: STREAM_TEST_FEHLER={type(e).__name__}: {e}")

finally:
    print("RESULT: STOP_STREAM")

    try:
        camera.stop_stream("mainStream")
        print("RESULT: STOP_STREAM_OK")
    except Exception as e:
        print(f"RESULT: STOP_STREAM_FEHLER={type(e).__name__}: {e}")

    try:
        camera.close()
        print("RESULT: CLOSE_OK")
    except Exception as e:
        print(f"RESULT: CLOSE_FEHLER={type(e).__name__}: {e}")

print("RESULT: TEST_ENDE")
PYTHON

echo "RESULT: PYTHON_DATEI_ERSTELLT"
echo "RESULT: STARTE_PYTHON"

python3 /data/reolink_raw_stream_analyse.py

EXITCODE=$?

echo "RESULT: PYTHON_EXITCODE=$EXITCODE"
echo "RESULT: SHELL_ENDE"
