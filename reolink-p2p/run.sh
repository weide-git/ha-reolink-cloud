#!/bin/sh

set -eu

echo "========================================"
echo " RESULT: PyNeolink API Diagnose"
echo "========================================"

python - <<'PY'
import sys
import inspect
import pkgutil

print("RESULT: Python=" + sys.version.replace("\n", " "))

try:
    import pyneolink

    print("RESULT: PYNEOLINK_FILE=" + str(pyneolink.__file__))
    print("RESULT: PYNEOLINK_VERSION=" + str(
        getattr(pyneolink, "__version__", "NICHT_VORHANDEN")
    ))

except Exception as e:
    print("RESULT: PYNEOLINK_IMPORT_ERROR=" + repr(e))
    sys.exit(1)


print("RESULT: STREAMSERVER_BEGIN")

try:
    from pyneolink import StreamServer

    print("RESULT: STREAMSERVER_CLASS=" + repr(StreamServer))

    try:
        print(
            "RESULT: STREAMSERVER_SIGNATURE="
            + str(inspect.signature(StreamServer))
        )
    except Exception as e:
        print(
            "RESULT: STREAMSERVER_SIGNATURE_ERROR="
            + repr(e)
        )

    try:
        doc = inspect.getdoc(StreamServer)
        if doc:
            for line in doc.splitlines():
                print("RESULT: STREAMSERVER_DOC=" + line)
        else:
            print("RESULT: STREAMSERVER_DOC=NONE")
    except Exception as e:
        print(
            "RESULT: STREAMSERVER_DOC_ERROR="
            + repr(e)
        )

except Exception as e:
    print("RESULT: STREAMSERVER_IMPORT_ERROR=" + repr(e))


print("RESULT: STREAMSERVER_END")
print("RESULT: MODULES_BEGIN")

try:
    import pyneolink

    for module in pkgutil.walk_packages(
        pyneolink.__path__,
        pyneolink.__name__ + "."
    ):
        print("RESULT: MODULE=" + module.name)

except Exception as e:
    print("RESULT: MODULE_SCAN_ERROR=" + repr(e))


print("RESULT: MODULES_END")
print("RESULT: DIAGNOSE_END")
PY

echo "========================================"
echo " RESULT: Shell Ende"
echo "========================================"
