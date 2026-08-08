#!/bin/sh

set -eu

OPTIONS="/data/options.json"

UID_VALUE="$(jq -r '.uid' "$OPTIONS")"
USERNAME_VALUE="$(jq -r '.username' "$OPTIONS")"
PASSWORD_VALUE="$(jq -r '.password' "$OPTIONS")"

echo "========================================"
echo " Reolink P2P Stream Timeout Test"
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

cat > /data/pyneolink/start_stream.py <<'PY'
import json
import signal
import sys
import traceback

from pyneolink import StreamServer

CONFIG_FILE = "/data/pyneolink/config.json"

print("========================================")
print(" PyNeolink StreamServer Test")
print("========================================")
print()

print("Lese Konfiguration ...")

with open(CONFIG_FILE, "r", encoding="utf-8") as f:
    config = json.load(f)

print("Konfiguration gelesen.")
print("Kamera:", config["cameras"][0]["name"])
print("UID:", config["cameras"][0]["uid"])
print("Discovery:", config["cameras"][0].get("discovery"))
print("Bind:", config["bind"])
print("Port:", config["bind_port"])
print()

print("Erzeuge StreamServer ...")

try:
    server = StreamServer(
        config,
        buffer_seconds=1.5,
        hls_buffer_mb=100,
        hls_segment_seconds=2,
    )

    print("StreamServer wurde erzeugt.")
    print()

except Exception as e:
    print("FEHLER beim Erzeugen des StreamServers:")
    print(type(e).__name__, str(e))
    traceback.print_exc()
    sys.exit(1)


def timeout_handler(signum, frame):
    print()
    print("========================================")
    print(" TIMEOUT")
    print("========================================")
    print()
    print("Nach 15 Sekunden wurde kein weiterer")
    print("Fortschritt vom StreamServer gemeldet.")
    print()
    print("Der Prozess wird jetzt beendet.")
    sys.exit(124)


signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(15)

print("Starte server.serve_forever() ...")
print("Timeout: 15 Sekunden")
print()

try:
    server.serve_forever()

except Exception as e:
    print()
    print("========================================")
    print(" FEHLER IM STREAMSERVER")
    print("========================================")
    print()
    print(type(e).__name__, str(e))
    traceback.print_exc()
    sys.exit(1)

finally:
    signal.alarm(0)

print()
print("========================================")
print(" STREAMSERVER BEENDET")
print("========================================")
PY

echo "========================================"
echo " Starte Live-Stream-Test"
echo "========================================"
echo

python /data/pyneolink/start_stream.py

RESULT=$?

echo
echo "========================================"
echo " TEST ENDE"
echo " Exit-Code: ${RESULT}"
echo "========================================"

exit "$RESULT"
