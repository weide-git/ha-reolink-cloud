#!/bin/sh

set -eu

OPTIONS="/data/options.json"

UID_VALUE="$(jq -r '.uid' "$OPTIONS")"
USERNAME_VALUE="$(jq -r '.username' "$OPTIONS")"
PASSWORD_VALUE="$(jq -r '.password' "$OPTIONS")"

OUT="/data/reolink_test.mp4"

rm -f "$OUT"

echo "========================================"
echo " Reolink DIREKTER P2P STREAM TEST"
echo "========================================"
echo
echo "UID: ${UID_VALUE}"
echo "Benutzer: ${USERNAME_VALUE}"
echo "Discovery: relay"
echo
echo "PyNeolink:"
python -c 'import pyneolink; print(getattr(pyneolink, "__version__", "unbekannt"))'
echo
echo "========================================"
echo " Starte Kamera"
echo "========================================"

python - <<PY
import sys
import time
import traceback

from pyneolink.camera import Camera
from pyneolink.camera import StreamRecorder

uid = "${UID_VALUE}"
username = "${USERNAME_VALUE}"
password = "${PASSWORD_VALUE}"

print("RESULT: CAMERA_ERSTELLEN")

camera = Camera(
    uid=uid,
    username=username,
    password=password,
    discovery="relay",
    stream="both",
    timeout=30.0,
    debug=True,
)

print("RESULT: CAMERA_ERSTELLT")
print("RESULT: STARTE_STREAM=SUBSTREAM")
print("RESULT: ZIEL=/data/reolink_test.mp4")

try:
    recorder = StreamRecorder(
        camera,
        out="/data/reolink_test.mp4",
        stream="subStream",
        duration=10.0,
    )

    print("RESULT: RECORDER_ERSTELLT")
    print("RESULT: STARTE_AUFNAHME")

    recorder.start()

    print("RESULT: AUFNAHME_GESTARTET")

    start = time.time()

    while time.time() - start < 15:
        time.sleep(1)
        print(
            "RESULT: WARTE="
            + str(int(time.time() - start))
            + "s"
        )

    print("RESULT: WARTEZEIT_ERREICHT")

except Exception as e:
    print("RESULT: STREAM_FEHLER=" + repr(e))
    traceback.print_exc()
    sys.exit(2)

finally:
    try:
        recorder.stop()
        print("RESULT: RECORDER_STOP")
    except Exception as e:
        print("RESULT: RECORDER_STOP_FEHLER=" + repr(e))

    try:
        camera.close()
        print("RESULT: CAMERA_CLOSE")
    except Exception as e:
        print("RESULT: CAMERA_CLOSE_FEHLER=" + repr(e))

print("RESULT: TEST_ENDE")
PY

echo
echo "========================================"
echo " Ergebnis"
echo "========================================"

if [ -f "$OUT" ]; then
    SIZE="$(stat -c '%s' "$OUT" 2>/dev/null || echo 0)"
    echo "RESULT: DATEI_VORHANDEN=JA"
    echo "RESULT: DATEIGROESSE=${SIZE}"

    if [ "$SIZE" -gt 0 ]; then
        echo "RESULT: VIDEO_DATEN=JA"
    else
        echo "RESULT: VIDEO_DATEN=NEIN"
    fi
else
    echo "RESULT: DATEI_VORHANDEN=NEIN"
fi

echo
echo "RESULT: TEST_ABGESCHLOSSEN"
