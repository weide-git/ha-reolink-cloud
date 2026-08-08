#!/bin/sh

echo "========================================"
echo " REOLINK P2P RAW STREAM TEST"
echo "========================================"

cat > /data/reolink_raw_stream_test.py <<'PYTHON'
import os
import time
from pyneolink.camera import Camera

UID = "9527000KLBT71M83"
USERNAME = "admin"
PASSWORD = os.environ.get("REOLINK_PASSWORD", "")

OUT = "/data/reolink_stream.bin"

print("RESULT: PYTHON_START")
print("RESULT: PYNEOLINK_IMPORT_OK")

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

    print("RESULT: START_STREAM")
    camera.start_stream("mainStream")
    print("RESULT: START_STREAM_OK")

    total = 0
    packets = 0
    start = time.time()

    print("RESULT: READ_STREAM_START")

    with open(OUT, "wb") as f:
        for payload in camera.read_stream_payloads("mainStream"):
            if payload:
                f.write(payload)
                f.flush()

                packets += 1
                total += len(payload)

                print(
                    f"RESULT: PAYLOAD={packets} "
                    f"BYTES={len(payload)} "
                    f"TOTAL={total}"
                )

            if time.time() - start >= 10:
                print("RESULT: 10_SEKUNDEN_ERREICHT")
                break

except Exception as e:
    print(f"RESULT: STREAM_FEHLER={type(e).__name__}: {e}")

finally:
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

print(f"RESULT: DATEI_VORHANDEN={os.path.exists(OUT)}")

if os.path.exists(OUT):
    print(f"RESULT: DATEIGROESSE={os.path.getsize(OUT)}")

print("RESULT: TEST_ENDE")
PYTHON

echo "RESULT: PYTHON_DATEI_ERSTELLT"
echo "RESULT: STARTE_PYTHON"

python3 /data/reolink_raw_stream_test.py

echo "RESULT: PYTHON_EXITCODE=$?"
echo "RESULT: SHELL_ENDE"
