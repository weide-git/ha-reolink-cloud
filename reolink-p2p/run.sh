#!/bin/sh

set -eu

OPTIONS="/data/options.json"

UID_VALUE="$(jq -r '.uid' "$OPTIONS")"
USERNAME_VALUE="$(jq -r '.username' "$OPTIONS")"
PASSWORD_VALUE="$(jq -r '.password' "$OPTIONS")"

echo "========================================"
echo " Reolink P2P Authentication Test"
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
echo " Konfiguration"
echo "========================================"
echo
echo "UID: ${UID_VALUE}"
echo "Username: ${USERNAME_VALUE}"
echo "Discovery: relay"
echo "Password: [VERBORGEN]"
echo

echo "========================================"
echo " P2P Login / Info"
echo "========================================"
echo

python /usr/local/lib/python3.12/site-packages/pyneolink/cli.py \
  info \
  --camera "RLC-510WA" \
  --config /data/pyneolink/config.json

RESULT=$?

echo
echo "========================================"
echo " Ergebnis"
echo "========================================"
echo "Exit-Code: ${RESULT}"
echo

exit ${RESULT}
