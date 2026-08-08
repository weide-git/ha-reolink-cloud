#!/bin/sh

set -eu

echo "========================================"
echo " PyNeolink Versions- und API-Diagnose"
echo "========================================"
echo

python - <<'PY'
import sys
import inspect

print("Python:")
print(sys.version)
print()

try:
    import pyneolink

    print("PyNeolink Modul:")
    print(pyneolink.__file__)
    print()

    print("PyNeolink Version:")
    print(getattr(pyneolink, "__version__", "nicht vorhanden"))
    print()

except Exception as e:
    print("FEHLER beim Import von pyneolink:")
    print(type(e).__name__, str(e))
    raise

print("========================================")
print(" StreamServer")
print("========================================")
print()

try:
    from pyneolink import StreamServer

    print("StreamServer:")
    print(StreamServer)
    print()

    print("Signatur:")
    print(inspect.signature(StreamServer))
    print()

    print("Dokumentation:")
    print(inspect.getdoc(StreamServer) or "Keine Dokumentation vorhanden")
    print()

except Exception as e:
    print("FEHLER bei StreamServer:")
    print(type(e).__name__, str(e))
    print()

print("========================================")
print(" PyNeolink Module")
print("========================================")
print()

try:
    import pkgutil
    import pyneolink

    for module in pkgutil.walk_packages(
        pyneolink.__path__,
        pyneolink.__name__ + "."
    ):
        print(module.name)

except Exception as e:
    print("Fehler beim Auflisten:")
    print(type(e).__name__, str(e))

print()

print("========================================")
print(" ENDE DER DIAGNOSE")
print("========================================")
