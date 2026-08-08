#!/bin/sh

set -eu

echo "========================================"
echo " Reolink UID/P2P Test"
echo "========================================"

mkdir -p /data

cat > /data/config.json <<EOF
{
  "bind": "0.0.0.0",
  "bind_port": 8554,
  "cameras": [
    {
      "name": "RLC-510WA",
      "username": "${USERNAME}",
      "password": "${PASSWORD}",
      "uid": "${UID}",
      "discovery": "relay"
    }
  ]
}
EOF

echo "UID: ${UID}"
echo "Benutzer: ${USERNAME}"
echo "P2P Discovery: relay"
echo
echo "Starte Verbindungstest..."
echo

exec python /app/pyneolink/cli.py info \
  --camera "RLC-510WA" \
  --config /data/config.json
