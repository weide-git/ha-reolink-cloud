#!/bin/sh

set -eu

OPTIONS="/data/options.json"

UID_VALUE="$(jq -r '.uid' "$OPTIONS")"
USERNAME_VALUE="$(jq -r '.username' "$OPTIONS")"
PASSWORD_VALUE="$(jq -r '.password' "$OPTIONS")"

echo "========================================"
echo " Reolink P2P CLI Test"
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

PYNEOLINK="/usr/local/lib/python3.12/site-packages/pyneolink/cli.py"

echo "========================================"
echo " PyNeolink CLI"
echo "========================================"
echo

python "$PYNEOLINK" --help 2>&1 || true

echo
echo "========================================"
echo " PyNeolink Info"
echo "========================================"
echo

python "$PYNEOLINK" \
  info \
  --camera "RLC-510WA" \
  --config /data/pyneolink/config.json

echo
echo "========================================"
echo " ENDE"
echo "========================================"
