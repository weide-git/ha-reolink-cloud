import os
import time
import traceback

from pyneolink.camera import Camera


print("========================================")
print(" REOLINK P2P RAW UDP STREAM TEST")
print("========================================")

print("RESULT: PYTHON_START")

# --------------------------------------------------
# Optionen lesen
# --------------------------------------------------

options = {}

options_file = "/data/options.json"

try:
    import json

    if os.path.exists(options_file):
        with open(options_file, "r", encoding="utf-8") as f:
            options = json.load(f)

    print("RESULT: OPTIONS_GELESEN")

except Exception as exc:
    print(f"RESULT: OPTIONS_FEHLER={type(exc).__name__}: {exc}")

uid = options.get("uid", "")
username = options.get("username", "admin")
password = options.get("password", "")

print(f"RESULT: UID={uid}")
print(f"RESULT: USERNAME={username}")
print(f"RESULT: PASSWORD_GESETZT={'JA' if password else 'NEIN'}")

if password:
    print(f"RESULT: PASSWORD_LAENGE={len(password)}")

# --------------------------------------------------
# Kamera erzeugen
# --------------------------------------------------

camera = None

try:
    camera = Camera(
        uid=uid,
        username=username,
        password=password,
    )

    print("RESULT: CAMERA_ERZEUGT")

except Exception as exc:
    print(f"RESULT: CAMERA_FEHLER={type(exc).__name__}: {exc}")
    traceback.print_exc()
    print("RESULT: PYTHON_ENDE")
    raise SystemExit(1)

# --------------------------------------------------
# CONNECT
# --------------------------------------------------

try:
    print("RESULT: CONNECT_START")

    camera.connect()

    print("RESULT: CONNECT_OK")

except Exception as exc:
    print(f"RESULT: CONNECT_FEHLER={type(exc).__name__}: {exc}")
    traceback.print_exc()

    try:
        camera.close()
    except Exception:
        pass

    print("RESULT: PYTHON_ENDE")
    raise SystemExit(1)

# --------------------------------------------------
# LOGIN
# --------------------------------------------------

try:
    print("RESULT: LOGIN_START")

    result = camera.login()

    print("RESULT: LOGIN_OK")
    print(f"RESULT: LOGIN_RESULT_TYPE={type(result)}")

except Exception as exc:
    print(f"RESULT: LOGIN_FEHLER={type(exc).__name__}: {exc}")
    traceback.print_exc()

    try:
        camera.close()
    except Exception:
        pass

    print("RESULT: PYTHON_ENDE")
    raise SystemExit(1)

# --------------------------------------------------
# STREAM STARTEN
# --------------------------------------------------

try:
    print("RESULT: START_STREAM")

    camera.start_stream("mainStream")

    print("RESULT: START_STREAM_OK")

except Exception as exc:
    print(f"RESULT: START_STREAM_FEHLER={type(exc).__name__}: {exc}")
    traceback.print_exc()

    try:
        camera.close()
    except Exception:
        pass

    print("RESULT: PYTHON_ENDE")
    raise SystemExit(1)

# --------------------------------------------------
# RAW UDP SOCKET TEST
# --------------------------------------------------

packets = 0
total_bytes = 0

try:
    print("RESULT: SOCKET_TYPE=" + str(type(camera.sock)))

    print("RESULT: RAW_SOCKET_TEST")

    # Wir lesen absichtlich direkt vom PyNeolink-Socket.
    #
    # Damit testen wir:
    # P2P-Verbindung
    # Login
    # Streamstart
    # UDP-Datenübertragung
    #
    # Es wird zunächst NICHT versucht, den H264-Stream
    # zu dekodieren.

    for attempt in range(10):

        print(f"RESULT: RECV_ATTEMPT={attempt + 1}")

        try:

            msg = camera._recv(timeout=3.0)

            packets += 1

            payload = getattr(msg, "payload", b"")

            if payload is None:
                payload = b""

            payload_len = len(payload)

            total_bytes += payload_len

            print("RESULT: RECV_OK=1")
            print(f"RESULT: MSG_TYPE={type(msg)}")
            print(f"RESULT: MSG_ID={getattr(msg, 'header', None)}")
            print(f"RESULT: PAYLOAD_LEN={payload_len}")
            print(f"RESULT: PACKETS={packets}")
            print(f"RESULT: BYTES={total_bytes}")

            # Erste Bytes ausgeben, damit wir sehen können,
            # ob tatsächlich H264-Daten ankommen.

            if payload:
                first = payload[:32].hex()
                print(f"RESULT: PAYLOAD_FIRST_32={first}")

                # H264 Annex-B Startcodes:
                # 00 00 01
                # oder
                # 00 00 00 01

                if (
                    b"\x00\x00\x01" in payload[:32]
                    or b"\x00\x00\x00\x01" in payload[:32]
                ):
                    print("RESULT: H264_STARTCODE=JA")
                else:
                    print("RESULT: H264_STARTCODE=NEIN")

        except Exception as exc:

            print(
                f"RESULT: RECV_FEHLER="
                f"{type(exc).__name__}: {exc}"
            )

            # Bei einem Timeout weitermachen.
            # So sehen wir, ob später noch Pakete kommen.

            if type(exc).__name__ == "TimeoutError":
                continue

            # Bei anderen Fehlern ebenfalls abbrechen,
            # aber den Fehler sauber protokollieren.

            traceback.print_exc()
            break

except Exception as exc:

    print(
        f"RESULT: RAW_TEST_FEHLER="
        f"{type(exc).__name__}: {exc}"
    )

    traceback.print_exc()

finally:

    print("RESULT: RAW_RECV_ENDE")
    print(f"RESULT: PACKETS={packets}")
    print(f"RESULT: BYTES={total_bytes}")

# --------------------------------------------------
# STREAM STOPPEN
# --------------------------------------------------

try:

    print("RESULT: STOP_STREAM")

    camera.stop_stream("mainStream")

    print("RESULT: STOP_STREAM_OK")

except Exception as exc:

    print(
        f"RESULT: STOP_STREAM_FEHLER="
        f"{type(exc).__name__}: {exc}"
    )

# --------------------------------------------------
# Verbindung schließen
# --------------------------------------------------

try:

    camera.close()

    print("RESULT: CLOSE_OK")

except Exception as exc:

    print(
        f"RESULT: CLOSE_FEHLER="
        f"{type(exc).__name__}: {exc}"
    )

print("RESULT: TEST_ENDE")
print("RESULT: PYTHON_ENDE")
