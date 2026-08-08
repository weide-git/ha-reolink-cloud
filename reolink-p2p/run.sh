#!/bin/sh

set -eu

OPTIONS="/data/options.json"

UID_VALUE="$(jq -r '.uid' "$OPTIONS")"
USERNAME_VALUE="$(jq -r '.username' "$OPTIONS")"
PASSWORD_VALUE="$(jq -r '.password' "$OPTIONS")"

echo "========================================"
echo " Reolink UID/P2P Test"
echo "========================================"
echo "UID: ${UID_VALUE}"
echo "Benutzer: ${USERNAME_VALUE}"
echo "P2P Discovery: relay"
echo
echo "Erstelle PyNeolink-Konfiguration..."

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
echo "Starte P2P-Informationstest..."
echo

exec python /usr/local/lib/python3.12/site-packages/pyneolink/cli.py \
  info \
  --camera "RLC-510WA" \
  --config /data/pyneolink/config.json
