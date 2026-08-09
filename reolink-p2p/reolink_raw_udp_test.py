import json
import os
import sys
import traceback

print("RESULT: PYTHON_START")

try:
    import pyneolink

    print("RESULT: PYNEOLINK_VERSION=" + getattr(pyneolink, "__version__", "unknown"))
    print("RESULT: CAMERA_IMPORT_OK")

except Exception as e:
    print("RESULT: IMPORT_FEHLER=" + repr(e))
    traceback.print_exc()
    sys.exit(0)


OPTIONS_FILE = "/data/options.json"

try:
    with open(OPTIONS_FILE, "r", encoding="utf-8") as f:
        options = json.load(f)

    print("RESULT: OPTIONS_GELESEN")

except Exception as e:
    print("RESULT: OPTIONS_FEHLER=" + repr(e))
    sys.exit(0)


uid = options.get("uid", "")
username = options.get("username", "admin")
password = options.get("password", "")

print("RESULT: UID=" + str(uid))
print("RESULT: USERNAME=" + str(username))
print("RESULT: PASSWORD_GESETZT=" + ("JA" if password else "NEIN"))

try:
    camera = pyneolink.Camera(
        uid=uid,
        username=username,
        password=password,
        timeout=30,
        debug=True,
    )

    print("RESULT: CAMERA_ERZEUGT")

except Exception as e:
    print("RESULT: CAMERA_ERZEUGUNG_FEHLER=" + repr(e))
    traceback.print_exc()
    sys.exit(0)


print("RESULT: CONNECT_START")

try:
    camera.connect()

    print("RESULT: CONNECT_OK")

except TimeoutError as e:
    print("RESULT: CONNECT_TIMEOUT=JA")
    print("RESULT: CONNECT_FEHLER=" + repr(e))

except Exception as e:
    print("RESULT: CONNECT_FEHLER=" + repr(e))
    traceback.print_exc()

finally:
    try:
        camera.close()
        print("RESULT: CLOSE_OK")
    except Exception as e:
        print("RESULT: CLOSE_FEHLER=" + repr(e))


print("RESULT: TEST_ENDE")
print("RESULT: PYTHON_ENDE")
