#!/bin/sh

echo "========================================"
echo " REOLINK P2P LOGIN TEST"
echo "========================================"

PASSWORD="$(python3 -c '
import json
with open("/data/options.json", "r") as f:
    data = json.load(f)
print(data.get("password", ""))
')"

echo "RESULT: OPTIONS_GELESEN"

if [ -z "$PASSWORD" ]; then
    echo "RESULT: PASSWORD_LEER"
else
    echo "RESULT: PASSWORD_GESETZT"
    echo "RESULT: PASSWORD_LAENGE=${#PASSWORD}"
fi

export REOLINK_PASSWORD="$PASSWORD"

cat > /data/reolink_login_test.py <<'PYTHON'
import os
import pyneolink

from pyneolink.camera import Camera


UID = "9527000KLBT71M83"
USERNAME = "admin"
PASSWORD = os.environ.get("REOLINK_PASSWORD", "")


print("RESULT: PYTHON_START")
print(f"RESULT: PYNEOLINK_VERSION={getattr(pyneolink, '__version__', 'unbekannt')}")
print("RESULT: CAMERA_IMPORT_OK")

print(f"RESULT: PASSWORD_GESETZT={bool(PASSWORD)}")
print(f"RESULT: PASSWORD_LAENGE={len(PASSWORD)}")

print("RESULT: ERZEUGE_CAMERA")

camera = Camera(
    uid=UID,
    username=USERNAME,
    password=PASSWORD,
    discovery="relay",
    stream="both",
    debug=True,
)

print("RESULT: CAMERA_ERZEUGT")
print(f"RESULT: CAMERA_TYP={type(camera)}")

try:
    print("RESULT: CONNECT_START")

    camera.connect()

    print("RESULT: CONNECT_OK")

    print("RESULT: LOGIN_START")

    result = camera.login()

    print("RESULT: LOGIN_OK")
    print(f"RESULT: LOGIN_RESULT={result}")

except Exception as e:
    print(f"RESULT: LOGIN_FEHLER={type(e).__name__}: {e}")

finally:
    try:
        camera.close()
        print("RESULT: CLOSE_OK")
    except Exception as e:
        print(f"RESULT: CLOSE_FEHLER={type(e).__name__}: {e}")

print("RESULT: TEST_ENDE")
PYTHON

echo "RESULT: PYTHON_DATEI_ERSTELLT"
echo "RESULT: STARTE_PYTHON"

python3 /data/reolink_login_test.py

EXITCODE=$?

echo "RESULT: PYTHON_EXITCODE=$EXITCODE"
echo "RESULT: SHELL_ENDE"
