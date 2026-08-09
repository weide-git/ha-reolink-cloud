import json
import sys
import inspect
import socket

print("RESULT: PYTHON_START", flush=True)

print("RESULT: IMPORT_START", flush=True)

import pyneolink
import pyneolink.core.udp_transport as udp
from pyneolink.camera import Camera

print("RESULT: IMPORT_OK", flush=True)
print(
"RESULT: PYNEOLINK_VERSION="
+ str(getattr(pyneolink, "**version**", "unbekannt")),
flush=True,
)

print("RESULT: OPTIONS_START", flush=True)

with open("/data/options.json", "r", encoding="utf-8") as f:
options = json.load(f)

uid = options.get("uid", "")
username = options.get("username", "admin")
password = options.get("password", "")

print("RESULT: UID=" + str(uid), flush=True)
print("RESULT: USERNAME=" + str(username), flush=True)
print(
"RESULT: PASSWORD_GESETZT="
+ ("JA" if password else "NEIN"),
flush=True,
)
print(
"RESULT: PASSWORD_LAENGE="
+ str(len(password)),
flush=True,
)

print("RESULT: UDP_TRANSPORT_START", flush=True)

names = sorted(
name for name in dir(udp)
if not name.startswith("__")
)

print(
"RESULT: UDP_OBJECT_COUNT="
+ str(len(names)),
flush=True,
)

for name in names:
try:
obj = getattr(udp, name)

```
    if inspect.isfunction(obj):
        try:
            sig = inspect.signature(obj)
        except Exception:
            sig = "unbekannt"

        print(
            "RESULT: UDP_FUNCTION="
            + name
            + " SIGNATURE="
            + str(sig),
            flush=True,
        )

    elif inspect.isclass(obj):
        print(
            "RESULT: UDP_CLASS="
            + name,
            flush=True,
        )

except Exception as exc:
    print(
        "RESULT: UDP_INSPECT_FEHLER="
        + name
        + " "
        + type(exc).__name__
        + ": "
        + str(exc),
        flush=True,
    )
```

print("RESULT: UDP_TRANSPORT_ENDE", flush=True)

print("RESULT: IMPORTANT_FUNCTIONS_START", flush=True)

for name in [
"connect_relay",
"connect_local",
"p2p_lookup",
"register_client",
"send_c2r",
"lookup",
"register",
]:
obj = getattr(udp, name, None)

```
if obj is None:
    print(
        "RESULT: FUNCTION="
        + name
        + " NICHT_VORHANDEN",
        flush=True,
    )
else:
    try:
        sig = inspect.signature(obj)
    except Exception:
        sig = "unbekannt"

    print(
        "RESULT: FUNCTION="
        + name
        + " VORHANDEN SIGNATURE="
        + str(sig),
        flush=True,
    )
```

print("RESULT: IMPORTANT_FUNCTIONS_ENDE", flush=True)

print("RESULT: CAMERA_ANALYSE_START", flush=True)

print(
"RESULT: CAMERA_CONNECT_SIGNATURE="
+ str(inspect.signature(Camera.connect)),
flush=True,
)

print(
"RESULT: CAMERA_LOGIN_SIGNATURE="
+ str(inspect.signature(Camera.login)),
flush=True,
)

print(
"RESULT: CAMERA_START_STREAM_SIGNATURE="
+ str(inspect.signature(Camera.start_stream)),
flush=True,
)

print("RESULT: CAMERA_METHODS_START", flush=True)

camera_methods = sorted(
name for name in dir(Camera)
if not name.startswith("__")
)

for name in camera_methods:
try:
obj = getattr(Camera, name)

```
    if callable(obj):
        try:
            sig = inspect.signature(obj)
        except Exception:
            sig = "unbekannt"

        print(
            "RESULT: CAMERA_METHOD="
            + name
            + " SIGNATURE="
            + str(sig),
            flush=True,
        )

except Exception:
    pass
```

print("RESULT: CAMERA_METHODS_ENDE", flush=True)

print("RESULT: CAMERA_OBJECT_START", flush=True)

camera = Camera(
uid=uid,
username=username,
password=password,
)

print("RESULT: CAMERA_OBJECT_OK", flush=True)

print("RESULT: NETWORK_START", flush=True)

hostname = socket.gethostname()

print(
"RESULT: HOSTNAME="
+ hostname,
flush=True,
)

try:
addresses = socket.getaddrinfo(
hostname,
None,
socket.AF_INET,
)

```
found = sorted(
    set(
        item[4][0]
        for item in addresses
        if item[4]
    )
)

for address in found:
    print(
        "RESULT: LOCAL_IPV4="
        + address,
        flush=True,
    )
```

except Exception as exc:
print(
"RESULT: LOCAL_IPV4_FEHLER="
+ type(exc).**name**
+ ": "
+ str(exc),
flush=True,
)

print("RESULT: NETWORK_ENDE", flush=True)

print("RESULT: UDP_SOCKET_START", flush=True)

sock = socket.socket(
socket.AF_INET,
socket.SOCK_DGRAM,
)

sock.settimeout(2.0)

sock.bind(
("0.0.0.0", 0)
)

local_ip, local_port = sock.getsockname()

print(
"RESULT: UDP_SOCKET_OK="
+ str(local_ip)
+ ":"
+ str(local_port),
flush=True,
)

sock.close()

print("RESULT: UDP_SOCKET_ENDE", flush=True)

print("RESULT: CONNECT_TEST=NICHT_AUSGEFUEHRT", flush=True)
print("RESULT: CAMERA_CONNECT=NICHT_AUSGEFUEHRT", flush=True)
print("RESULT: TEST_ENDE", flush=True)
print("RESULT: PYTHON_ENDE", flush=True)

sys.exit(0)
