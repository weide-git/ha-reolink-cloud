#!/bin/sh

set -eu

OPTIONS="/data/options.json"

UID_VALUE="$(jq -r '.uid' "$OPTIONS")"
USERNAME_VALUE="$(jq -r '.username' "$OPTIONS")"
PASSWORD_VALUE="$(jq -r '.password' "$OPTIONS")"

echo "========================================"
echo " Reolink UID/P2P Live Server"
echo "========================================"
echo
echo "UID: ${UID_VALUE}"
echo "Benutzer: ${USERNAME_VALUE}"
echo "Passwort gesetzt: $(if [ -n "$PASSWORD_VALUE" ]; then echo JA; else echo NEIN; fi)"
echo

mkdir -p /data/pyneolink

cat > /data/pyneolink/start_stream.py <<'PY'
import json
import sys

from pyneolink import StreamServer

CONFIG_FILE = "/data/pyneolink/config.json"

with open(CONFIG_FILE, "r", encoding="utf-8") as f:
    config = json.load(f)

print("========================================")
print(" Starte PyNeolink StreamServer")
print("========================================")
print()
print("Bind-Adresse:", config["bind"])
print("RTSP/Stream-Port:", config["bind_port"])
print("Kamera:", config["cameras"][0]["name"])
print()

server = StreamServer(
    config,
    buffer_seconds=1.5,
    hls_buffer_mb=100,
    hls_segment_seconds=2,
)

print("StreamServer wird gestartet...")
print()

server.serve_forever()
PY

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

echo "Konfiguration erstellt."
echo

echo "========================================"
echo " Starte Live-Stream"
echo "========================================"
echo

python /data/pyneolink/start_stream.py
