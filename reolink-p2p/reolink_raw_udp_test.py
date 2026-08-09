import json
import sys
import traceback
import inspect
import socket

print("RESULT: PYTHON_START", flush=True)

# ============================================================

# IMPORT

# ============================================================

try:
import pyneolink
import pyneolink.core.udp_transport as udp

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

# ============================================================

# OPTIONEN

# ============================================================

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
    f"RESULT: PASSWORD_GESETZT={'JA' if password else 'NEIN'}",
    flush=True,
)
print(f"RESULT: PASSWORD_LAENGE={len(password)}", flush=True)
```

except Exception as exc:
print(
f"RESULT: OPTIONS_FEHLER={type(exc).**name**}: {exc}",
flush=True,
)
traceback.print_exc()
sys.exit(1)

# ============================================================

# UDP_TRANSPORT UNTERSUCHEN

# ============================================================

print("RESULT: UDP_TRANSPORT_ANALYSE_START", flush=True)

try:
names = sorted(
name
for name in dir(udp)
if not name.startswith("__")
)

```
print(
    f"RESULT: UDP_TRANSPORT_OBJECTS={len(names)}",
    flush=True,
)

for name in names:
    try:
        obj = getattr(udp, name)

        if inspect.isfunction(obj):
            print(
                f"RESULT: FUNCTION={name}"
                f" SIGNATURE={inspect.signature(obj)}",
                flush=True,
            )

        elif inspect.isclass(obj):
            print(
                f"RESULT: CLASS={name}",
                flush=True,
            )

    except Exception as exc:
        print(
            f"RESULT: INSPECT_FEHLER={name}: "
            f"{type(exc).__name__}: {exc}",
            flush=True,
        )
```

except Exception as exc:
print(
f"RESULT: UDP_ANALYSE_FEHLER={type(exc).**name**}: {exc}",
flush=True,
)
traceback.print_exc()

print("RESULT: UDP_TRANSPORT_ANALYSE_ENDE", flush=True)

# ============================================================

# WICHTIGE FUNKTIONEN DIREKT PRÜFEN

# ============================================================

for function_name in [
"connect_relay",
"connect_local",
"p2p_lookup",
"register_client",
"send_c2r",
]:
try:
obj = getattr(udp, function_name, None)

```
    if obj is None:
        print(
            f"RESULT: FUNCTION_CHECK={function_name}: NICHT_VORHANDEN",
            flush=True,
        )
    else:
        print(
            f"RESULT: FUNCTION_CHECK={function_name}: VORHANDEN",
            flush=True,
        )

        try:
            print(
                f"RESULT: FUNCTION_SIGNATURE={function_name}: "
                f"{inspect.signature(obj)}",
                flush=True,
            )
        except Exception:
            pass

except Exception as exc:
    print(
        f"RESULT: FUNCTION_CHECK_FEHLER={function_name}: "
        f"{type(exc).__name__}: {exc}",
        flush=True,
    )
```

# ============================================================

# CAMERA-KLASSE ANALYSIEREN

# ============================================================

try:
from pyneolink.camera import Camera

```
print("RESULT: CAMERA_CLASS_OK", flush=True)

print(
    f"RESULT: CAMERA_CONNECT_SIGNATURE="
    f"{inspect.signature(Camera.connect)}",
    flush=True,
)

print(
    f"RESULT: CAMERA_LOGIN_SIGNATURE="
    f"{inspect.signature(Camera.login)}",
    flush=True,
)

print(
    f"RESULT: CAMERA_STREAM_SIGNATURE="
    f"{inspect.signature(Camera.start_stream)}",
    flush=True,
)
```

except Exception as exc:
print(
f"RESULT: CAMERA_ANALYSE_FEHLER="
f"{type(exc).**name**}: {exc}",
flush=True,
)
traceback.print_exc()

# ============================================================

# SOCKET / NETZWERK INFORMATIONEN

# ============================================================

print("RESULT: NETWORK_ANALYSE_START", flush=True)

try:
hostname = socket.gethostname()
print(f"RESULT: HOSTNAME={hostname}", flush=True)

```
try:
    addresses = socket.getaddrinfo(
        hostname,
        None,
        socket.AF_INET,
    )

    unique_addresses = sorted(
        {
            entry[4][0]
            for entry in addresses
            if entry[4]
        }
    )

    for address in unique_addresses:
        print(
            f"RESULT: LOCAL_IPV4={address}",
            flush=True,
        )

except Exception as exc:
    print(
        f"RESULT: LOCAL_IP_FEHLER="
        f"{type(exc).__name__}: {exc}",
        flush=True,
    )
```

except Exception as exc:
print(
f"RESULT: NETWORK_FEHLER={type(exc).**name**}: {exc}",
flush=True,
)

# ============================================================

# SOCKET TEST

# ============================================================

try:
sock = socket.socket(
socket.AF_INET,
socket.SOCK_DGRAM,
)

```
sock.settimeout(2.0)

sock.bind(("0.0.0.0", 0))

local_ip, local_port = sock.getsockname()

print(
    f"RESULT: UDP_SOCKET_OK={local_ip}:{local_port}",
    flush=True,
)

sock.close()
```

except Exception as exc:
print(
f"RESULT: UDP_SOCKET_FEHLER="
f"{type(exc).**name**}: {exc}",
flush=True,
)

print("RESULT: NETWORK_ANALYSE_ENDE", flush=True)

# ============================================================

# CAMERA OBJEKT ERZEUGEN

# ============================================================

try:
camera = Camera(
uid=uid,
username=username,
password=password,
)

```
print("RESULT: CAMERA_ERZEUGT", flush=True)

# Nur Objektattribute untersuchen.
# Noch KEIN camera.connect()!

attrs = sorted(
    name
    for name in dir(camera)
    if not name.startswith("__")
)

print(
    f"RESULT: CAMERA_ATTRIBUTES={len(attrs)}",
    flush=True,
)

for name in attrs:
    try:
        obj = getattr(camera, name)

        if callable(obj):
            try:
                signature = inspect.signature(obj)
                print(
                    f"RESULT: CAMERA_METHOD={name}"
                    f" SIGNATURE={signature}",
                    flush=True,
                )
            except Exception:
                print(
                    f"RESULT: CAMERA_METHOD={name}",
                    flush=True,
                )

    except Exception:
        pass
```

except Exception as exc:
print(
f"RESULT: CAMERA_ERZEUGEN_FEHLER="
f"{type(exc).**name**}: {exc}",
flush=True,
)
traceback.print_exc()

# ============================================================

# ABSICHTLICH KEIN CONNECT

# ============================================================

print("RESULT: CONNECT_TEST=NICHT_AUSGEFUEHRT", flush=True)
print("RESULT: GRUND=ZUERST_PYNEOLINK_P2P_API_ANALYSIEREN", flush=True)

print("RESULT: TEST_ENDE", flush=True)
print("RESULT: PYTHON_ENDE", flush=True)

sys.exit(0)
