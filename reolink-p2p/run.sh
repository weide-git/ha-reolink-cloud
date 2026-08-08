#!/bin/sh

set -eu

OPTIONS="/data/options.json"

UID_VALUE="$(jq -r '.uid' "$OPTIONS")"
USERNAME_VALUE="$(jq -r '.username' "$OPTIONS")"
PASSWORD_VALUE="$(jq -r '.password' "$OPTIONS")"

echo "========================================"
echo " Reolink PyNeolink API Diagnose"
echo "========================================"
echo
echo "UID: ${UID_VALUE}"
echo "Benutzer: ${USERNAME_VALUE}"
echo "Passwort gesetzt: $(if [ -n "$PASSWORD_VALUE" ]; then echo JA; else echo NEIN; fi)"
echo

mkdir -p /data/pyneolink

cat > /data/pyneolink/config.json <<EOF
{
  "bind": "0.0.0.0",
  "bind_port": 8554,
  "cameras": [
    {
      "name": "RLC-510WA",
      "username": "${USERNAME_VALUE}",
      "password": "${PASSWORD_VALUE}",
      "uid": "${UID_VALUE}",
      "discovery": "relay"
    }
  ]
}
EOF

echo "========================================"
echo " Installierte PyNeolink-Dateien"
echo "========================================"
echo

python - <<'PY'
import pyneolink
import os

print("PyNeolink Modul:")
print(pyneolink.__file__)
print()

base = os.path.dirname(pyneolink.__file__)

for root, dirs, files in os.walk(base):
    for file in files:
        if file.endswith(".py"):
            print(os.path.join(root, file))
PY

echo
echo "========================================"
echo " Relevante Funktionen / Klassen"
echo "========================================"
echo

python - <<'PY'
import pyneolink
import os

base = os.path.dirname(pyneolink.__file__)

keywords = [
    "stream",
    "snapshot",
    "video",
    "camera",
    "rtsp",
    "live"
]

for root, dirs, files in os.walk(base):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)

            try:
                with open(path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
            except Exception:
                continue

            for number, line in enumerate(lines, 1):
                lower = line.lower()

                if any(keyword in lower for keyword in keywords):
                    print(
                        f"{path}:{number}: "
                        f"{line.rstrip()}"
                    )
PY

echo
echo "========================================"
echo " ENDE DER API-DIAGNOSE"
echo "========================================"
