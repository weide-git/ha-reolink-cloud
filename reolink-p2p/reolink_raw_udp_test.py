print("RESULT: TEST_UMGEBUNG_START")
import json
import os
import sys
import traceback
import inspect

print("RESULT: PYTHON_START", flush=True)

# ------------------------------------------------------------

# PyNeolink importieren

# ------------------------------------------------------------

try:
import pyneolink
from pyneolink.camera import Camera
import pyneolink.core.udp_transport as udp_transport

```
print(
    f"RESULT: PYNEOLINK_VERSION="
    f"{getattr(pyneolink, '__version__', 'unbekannt')}",
    flush=True,
)

print("RESULT: CAMERA_IMPORT_OK", flush=True)
```

except Exception as exc:
print(
f"RESULT: IMPORT_FEHLER={type(exc).**name**}: {exc}",
flush=True,
)
traceback.print_exc()
sys.exit(1)

# ------------------------------------------------------------

# Installationspfade anzeigen

# ------------------------------------------------------------

try:
print(
f"RESULT: UDP_TRANSPORT_FILE={inspect.getfile(udp_transport)}",
flush=True,
)

```
print(
    f"RESULT: CAMERA_FILE={inspect.getfile(Camera)}",
    flush=True,
)
```

except Exception as exc:
print(
f"RESULT: PATH_FEHLER={type(exc).**name**}: {exc}",
flush=True,
)

# ------------------------------------------------------------

# Relevanten Teil von udp_transport.py ausgeben

# ------------------------------------------------------------

transport_file = inspect.getfile(udp_transport)

print("RESULT: UDP_TRANSPORT_SOURCE_START", flush=True)

try:
with open(transport_file, "r", encoding="utf-8") as f:
lines = f.readlines()

```
print(
    f"RESULT: UDP_TRANSPORT_LINE_COUNT={len(lines)}",
    flush=True,
)

# Zeilen 350-450 ausgeben.
# Falls die Datei kürzer ist, wird automatisch begrenzt.
start_line = 350
end_line = min(450, len(lines))

print(
    f"RESULT: SOURCE_LINES={start_line}-{end_line}",
    flush=True,
)

for number in range(start_line, end_line + 1):
    print(
        f"RESULT: SOURCE_{number:04d}="
        f"{lines[number - 1].rstrip()}",
        flush=True,
    )
```

except Exception as exc:
print(
f"RESULT: SOURCE_FEHLER={type(exc).**name**}: {exc}",
flush=True,
)
traceback.print_exc()

print("RESULT: UDP_TRANSPORT_SOURCE_END", flush=True)

# ------------------------------------------------------------

# Funktionen / Klassen des Moduls anzeigen

# ------------------------------------------------------------

print("RESULT: MODULE_FUNCTIONS_START", flush=True)

try:
for name in sorted(dir(udp_transport)):
if name.startswith("_"):
continue

```
    obj = getattr(udp_transport, name)

    if inspect.isfunction(obj):
        print(
            f"RESULT: FUNCTION={name}",
            flush=True,
        )

    elif inspect.isclass(obj):
        print(
            f"RESULT: CLASS={name}",
            flush=True,
        )
```

except Exception as exc:
print(
f"RESULT: MODULE_FUNCTIONS_FEHLER="
f"{type(exc).**name**}: {exc}",
flush=True,
)

print("RESULT: MODULE_FUNCTIONS_END", flush=True)

# ------------------------------------------------------------

# Optionen lesen

# ------------------------------------------------------------

print("RESULT: OPTIONS_START", flush=True)

try:
with open("/data/options.json", "r", encoding="utf-8") as f:
options = json.load(f)

```
uid = options.get("uid", "")
username = options.get("username", "admin")
password = options.get("password", "")

print(f"RESULT: UID={uid}", flush=True)
print(f"RESULT: USERNAME={username}", flush=True)
print(
    f"RESULT: PASSWORD_GESETZT="
    f"{'JA' if password else 'NEIN'}",
    flush=True,
)
print(
    f"RESULT: PASSWORD_LAENGE={len(password)}",
    flush=True,
)
```

except Exception as exc:
print(
f"RESULT: OPTIONS_FEHLER={type(exc).**name**}: {exc}",
flush=True,
)
traceback.print_exc()
sys.exit(1)

# ------------------------------------------------------------

# Kameraobjekt erzeugen

# ------------------------------------------------------------

camera = None

try:
camera = Camera(
uid=uid,
username=username,
password=password,
debug=True,
)

```
print("RESULT: CAMERA_ERZEUGT", flush=True)
```

except Exception as exc:
print(
f"RESULT: CAMERA_ERZEUGT_FEHLER="
f"{type(exc).**name**}: {exc}",
flush=True,
)
traceback.print_exc()
sys.exit(1)

# ------------------------------------------------------------

# Verbindung testen

# ------------------------------------------------------------

print("RESULT: CONNECT_START", flush=True)

try:
camera.connect()

```
print("RESULT: CONNECT_OK", flush=True)
```

except Exception as exc:
print(
f"RESULT: CONNECT_FEHLER={type(exc).**name**}: {exc}",
flush=True,
)

```
traceback.print_exc()

if type(exc).__name__ == "TimeoutError":
    print("RESULT: CONNECT_TIMEOUT=JA", flush=True)

print(
    "RESULT: CONNECTION_DETAILS_NICHT_ERMITTELT",
    flush=True,
)

try:
    if camera is not None:
        camera.close()
        print("RESULT: CLOSE_OK", flush=True)

except Exception as close_exc:
    print(
        f"RESULT: CLOSE_FEHLER="
        f"{type(close_exc).__name__}: {close_exc}",
        flush=True,
    )

print("RESULT: TEST_ENDE", flush=True)
print("RESULT: PYTHON_ENDE", flush=True)

sys.exit(0)
```

# ------------------------------------------------------------

# Nur falls Verbindung erfolgreich war

# ------------------------------------------------------------

print("RESULT: CONNECTION_ESTABLISHED", flush=True)

try:
sock = getattr(camera, "sock", None)

```
print(
    f"RESULT: SOCKET_TYPE={type(sock)}",
    flush=True,
)

if sock is not None:
    try:
        print(
            f"RESULT: SOCKET_LOCAL={sock.getsockname()}",
            flush=True,
        )
    except Exception:
        pass

    try:
        print(
            f"RESULT: SOCKET_PEER={sock.getpeername()}",
            flush=True,
        )
    except Exception:
        pass
```

except Exception as exc:
print(
f"RESULT: SOCKET_INFO_FEHLER="
f"{type(exc).**name**}: {exc}",
flush=True,
)

# ------------------------------------------------------------

# Aufräumen

# ------------------------------------------------------------

try:
camera.close()
print("RESULT: CLOSE_OK", flush=True)

except Exception as exc:
print(
f"RESULT: CLOSE_FEHLER="
f"{type(exc).**name**}: {exc}",
flush=True,
)

print("RESULT: TEST_ENDE", flush=True)
print("RESULT: PYTHON_ENDE", flush=True)
