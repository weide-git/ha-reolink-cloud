#!/bin/sh

set -eu

OPTIONS="/data/options.json"

UID_VALUE="$(jq -r '.uid' "$OPTIONS")"
USERNAME_VALUE="$(jq -r '.username' "$OPTIONS")"
PASSWORD_VALUE="$(jq -r '.password' "$OPTIONS")"

echo "========================================"
echo " Reolink UID/P2P Live Test"
echo "========================================"
echo "UID: ${UID_VALUE}"
echo "Benutzer: ${USERNAME_VALUE}"
echo "P2P Discovery: relay"
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

echo "Konfiguration erstellt."
echo

echo "========================================"
echo " Kamera-Verbindung"
echo "========================================"
echo

python /usr/local/lib/python3.12/site-packages/pyneolink/cli.py \
  info \
  --camera "RLC-510WA" \
  --config /data/pyneolink/config.json

echo
echo "========================================"
echo " Starte PyNeolink Live-Server"
echo "========================================"
echo
echo "RTSP-Port: 8554"
echo "Kamera: RLC-510WA"
echo
echo "Der Server bleibt jetzt aktiv."
echo

exec python /usr/local/lib/python3.12/site-packages/pyneolink/cli.py \
  live \
  --camera "RLC-510WA" \
  --config /data/pyneolink/config.json
