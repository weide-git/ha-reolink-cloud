#!/bin/sh

set -eu

echo "========================================"
echo " Reolink UID/P2P Test"
echo "========================================"

echo "UID: ${UID}"
echo "Benutzer: ${USERNAME}"
echo "Starte PyNeolink..."
echo

exec python -m pyneolink \
  --uid "${UID}" \
  --username "${USERNAME}" \
  --password "${PASSWORD}" \
  --discovery relay
