#!/bin/sh

echo "========================================"
echo " PYTHON STARTTEST"
echo "========================================"

echo "RESULT: 1 - SHELL START"

echo "RESULT: 2 - PYTHON AUFRUF"

python -u -c 'print("RESULT: 3 - PYTHON LAEUFT", flush=True)'

echo "RESULT: 4 - PYTHON BEENDET"

echo "RESULT: 5 - ENDE"
