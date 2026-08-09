import json
import sys
import time
import traceback

print("RESULT: PYTHON_START", flush=True)

try:
    import pyneolink

    print(
        "RESULT: PYNEOLINK_VERSION="
        + getattr(pyneolink, "__version__", "unknown"),
        flush=True,
    )
    print("RESULT: CAMERA_IMPORT_OK", flush=True)

except Exception as e:
    print("RESULT: IMPORT_FEHLER=" + repr(e), flush=True)
    traceback.print_exc()
    sys.exit(0)


OPTIONS_FILE = "/data/options.json"

try:
    with open(OPTIONS_FILE, "r", encoding="utf-8") as f:
        options = json.load(f)

    print("RESULT: OPTIONS_GELESEN", flush=True)

except Exception as e:
    print("RESULT: OPTIONS_FEHLER=" + repr(e), flush=True)
    sys.exit(0)


uid = options.get("uid", "")
username = options.get("username", "admin")
password = options.get("password", "")

print("RESULT: UID=" + str(uid), flush=True)
print("RESULT: USERNAME=" + str(username), flush=True)
print(
    "RESULT: PASSWORD_GESETZT=" + ("JA" if password else "NEIN"),
    flush=True,
)

try:
    print("RESULT: CAMERA_ERZEUGUNG_START", flush=True)

    camera = pyneolink.Camera(
        uid=uid,
        username=username,
        password=password,
        timeout=120,
        debug=True,
    )

    print("RESULT: CAMERA_ERZEUGT", flush=True)

except Exception as e:
    print("RESULT: CAMERA_ERZEUGUNG_FEHLER=" + repr(e), flush=True)
    traceback.print_exc()
    sys.exit(0)


print("RESULT: CONNECT_START", flush=True)
print("RESULT: CONNECT_TIMEOUT_SETTING=120", flush=True)

start = time.monotonic()

try:
    camera.connect()

    elapsed = time.monotonic() - start

    print(
        "RESULT: CONNECT_OK nach %.1f Sekunden" % elapsed,
        flush=True,
    )

except TimeoutError as e:
    elapsed = time.monotonic() - start

    print(
        "RESULT: CONNECT_TIMEOUT nach %.1f Sekunden" % elapsed,
        flush=True,
    )
    print("RESULT: CONNECT_FEHLER=" + repr(e), flush=True)

except Exception as e:
    elapsed = time.monotonic() - start

    print(
        "RESULT: CONNECT_FEHLER nach %.1f Sekunden" % elapsed,
        flush=True,
    )
    print("RESULT: CONNECT_FEHLER_DETAIL=" + repr(e), flush=True)
    traceback.print_exc()

finally:
    try:
        camera.close()
        print("RESULT: CLOSE_OK", flush=True)
    except Exception as e:
        print("RESULT: CLOSE_FEHLER=" + repr(e), flush=True)


print("RESULT: TEST_ENDE", flush=True)
print("RESULT: PYTHON_ENDE", flush=True)
