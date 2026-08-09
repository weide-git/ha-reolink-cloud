import json
import sys
import time
import traceback


def result(message):
    print(f"RESULT: {message}", flush=True)


result("PYTHON_START")

camera = None

# ------------------------------------------------------------
# PyNeolink import
# ------------------------------------------------------------

try:
    import pyneolink
    from pyneolink.camera import Camera

    result(
        f"PYNEOLINK_VERSION="
        f"{getattr(pyneolink, '__version__', 'unbekannt')}"
    )
    result("CAMERA_IMPORT_OK")

except Exception as exc:
    result(f"IMPORT_FEHLER={type(exc).__name__}: {exc}")
    traceback.print_exc()
    sys.exit(1)


# ------------------------------------------------------------
# Optionen lesen
# ------------------------------------------------------------

try:
    with open("/data/options.json", "r", encoding="utf-8") as file:
        options = json.load(file)

    uid = str(options.get("uid", "")).strip()
    username = str(options.get("username", "admin")).strip()
    password = str(options.get("password", ""))

    result(f"UID={uid}")
    result(f"USERNAME={username}")
    result(
        f"PASSWORD_GESETZT="
        f"{'JA' if password else 'NEIN'}"
    )
    result(f"PASSWORD_LAENGE={len(password)}")

    if not uid:
        result("FEHLER_UID_FEHLT")
        sys.exit(1)

    if not password:
        result("FEHLER_PASSWORT_FEHLT")
        sys.exit(1)

except Exception as exc:
    result(f"OPTIONS_FEHLER={type(exc).__name__}: {exc}")
    traceback.print_exc()
    sys.exit(1)


# ------------------------------------------------------------
# Kamera erzeugen
# ------------------------------------------------------------

try:
    result("CAMERA_ERZEUGT")

    camera = Camera(
        uid=uid,
        username=username,
        password=password,
        debug=True,
    )

    result("CAMERA_OBJEKT_OK")

except Exception as exc:
    result(f"CAMERA_ERZEUGEN_FEHLER={type(exc).__name__}: {exc}")
    traceback.print_exc()
    sys.exit(1)


# ------------------------------------------------------------
# CONNECT
# ------------------------------------------------------------

try:
    result("CONNECT_START")

    camera.connect()

    result("CONNECT_OK")

except Exception as exc:
    result(f"CONNECT_FEHLER={type(exc).__name__}: {exc}")
    traceback.print_exc()

    # Auch bei Connect-Fehler sauber schließen
    try:
        camera.close()
        result("CLOSE_OK")
    except Exception as close_exc:
        result(
            f"CLOSE_FEHLER="
            f"{type(close_exc).__name__}: {close_exc}"
        )

    result("TEST_ENDE")
    result("PYTHON_ENDE")
    sys.exit(2)


# ------------------------------------------------------------
# LOGIN
# ------------------------------------------------------------

try:
    result("LOGIN_START")

    login_result = camera.login()

    result("LOGIN_OK")
    result(f"LOGIN_RESULT_TYPE={type(login_result)}")

    if login_result is not None:
        login_text = str(login_result)

        result(f"LOGIN_RESULT_LEN={len(login_text)}")

        # Begrenzen, damit der Log nicht unnötig riesig wird.
        print(login_text[:4000], flush=True)

except Exception as exc:
    result(f"LOGIN_FEHLER={type(exc).__name__}: {exc}")
    traceback.print_exc()

    try:
        camera.close()
        result("CLOSE_OK")
    except Exception as close_exc:
        result(
            f"CLOSE_FEHLER="
            f"{type(close_exc).__name__}: {close_exc}"
        )

    result("TEST_ENDE")
    result("PYTHON_ENDE")
    sys.exit(3)


# ------------------------------------------------------------
# STREAM STARTEN
# ------------------------------------------------------------

try:
    result("START_STREAM")

    camera.start_stream("mainStream")

    result("START_STREAM_OK")

except Exception as exc:
    result(
        f"START_STREAM_FEHLER="
        f"{type(exc).__name__}: {exc}"
    )
    traceback.print_exc()

    try:
        camera.close()
        result("CLOSE_OK")
    except Exception as close_exc:
        result(
            f"CLOSE_FEHLER="
            f"{type(close_exc).__name__}: {close_exc}"
        )

    result("TEST_ENDE")
    result("PYTHON_ENDE")
    sys.exit(4)


# ------------------------------------------------------------
# Socket untersuchen
# ------------------------------------------------------------

result("STREAM_LAEUFT")

try:
    sock = getattr(camera, "sock", None)

    result(f"SOCKET_TYPE={type(sock)}")

    if sock is not None:

        attributes = [
            "addr",
            "camera_id",
            "client_id",
            "data_packets_received",
            "data_bytes_received",
            "acks_received",
            "acks_sent",
            "duplicate_packets_received",
            "ignored_packets",
            "unknown_packets",
        ]

        for attribute in attributes:
            try:
                value = getattr(sock, attribute)
                result(
                    f"SOCKET_{attribute.upper()}={value}"
                )
            except Exception:
                pass

except Exception as exc:
    result(
        f"SOCKET_ANALYSE_FEHLER="
        f"{type(exc).__name__}: {exc}"
    )


# ------------------------------------------------------------
# Stream laufen lassen
# ------------------------------------------------------------

result("STREAM_TEST_START")

for second in range(1, 16):

    time.sleep(1)

    try:
        sock = getattr(camera, "sock", None)

        if sock is None:
            result(
                f"STREAM_STATUS={second}s "
                f"SOCKET=NONE"
            )
            continue

        packets = getattr(
            sock,
            "data_packets_received",
            None,
        )

        bytes_received = getattr(
            sock,
            "data_bytes_received",
            None,
        )

        acks_received = getattr(
            sock,
            "acks_received",
            None,
        )

        acks_sent = getattr(
            sock,
            "acks_sent",
            None,
        )

        result(
            f"STREAM_STATUS={second}s "
            f"PACKETS={packets} "
            f"BYTES={bytes_received} "
            f"ACKS_RX={acks_received} "
            f"ACKS_TX={acks_sent}"
        )

    except Exception as exc:
        result(
            f"STREAM_STATUS_FEHLER="
            f"{type(exc).__name__}: {exc}"
        )


result("STREAM_TEST_ENDE")


# ------------------------------------------------------------
# Stream stoppen
# ------------------------------------------------------------

result("STOP_STREAM")

try:
    camera.stop_stream("mainStream")
    result("STOP_STREAM_OK")

except Exception as exc:
    result(
        f"STOP_STREAM_FEHLER="
        f"{type(exc).__name__}: {exc}"
    )
    traceback.print_exc()


# ------------------------------------------------------------
# Verbindung schließen
# ------------------------------------------------------------

try:
    camera.close()
    result("CLOSE_OK")

except Exception as exc:
    result(
        f"CLOSE_FEHLER="
        f"{type(exc).__name__}: {exc}"
    )


result("TEST_ENDE")
result("PYTHON_ENDE")
