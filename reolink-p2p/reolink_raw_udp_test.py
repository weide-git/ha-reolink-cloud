import json
import sys
import time
import traceback


def result(message):
    print(f"RESULT: {message}", flush=True)


result("PYTHON_START")

camera = None

try:
    import pyneolink
    from pyneolink.camera import Camera

    result(f"PYNEOLINK_VERSION={getattr(pyneolink, '__version__', 'unbekannt')}")
    result("CAMERA_IMPORT_OK")

except Exception as exc:
    result(f"IMPORT_FEHLER={type(exc).__name__}: {exc}")
    traceback.print_exc()
    sys.exit(1)


try:
    with open("/data/options.json", "r", encoding="utf-8") as file:
        options = json.load(file)

    uid = options.get("uid", "").strip()
    username = options.get("username", "admin").strip()
    password = options.get("password", "")

    result(f"UID={uid}")
    result(f"USERNAME={username}")
    result(f"PASSWORD_GESETZT={'JA' if password else 'NEIN'}")
    result(f"PASSWORD_LAENGE={len(password)}")

    if not uid:
        result("FEHLER_UID_FEHLT")
        sys.exit(1)

    if not password:
        result("FEHLER_PASSWORT_FEHLT")
        sys.exit(1)

    result("CAMERA_ERZEUGT")

    camera = Camera(
        uid=uid,
        username=username,
        password=password,
    )

    result("CONNECT_START")

    try:
        camera.connect()
        result("CONNECT_OK")

    except Exception as exc:
        result(f"CONNECT_FEHLER={type(exc).__name__}: {exc}")
        traceback.print_exc()
        sys.exit(2)

    result("LOGIN_START")

    try:
        login_result = camera.login()

        result("LOGIN_OK")
        result(f"LOGIN_RESULT_TYPE={type(login_result)}")

        if login_result is not None:
            text = str(login_result)
            result(f"LOGIN_RESULT_LEN={len(text)}")
            print(text[:4000], flush=True)

    except Exception as exc:
        result(f"LOGIN_FEHLER={type(exc).__name__}: {exc}")
        traceback.print_exc()
        sys.exit(3)

    result("START_STREAM")

    try:
        camera.start_stream("mainStream")
        result("START_STREAM_OK")

    except Exception as exc:
        result(f"START_STREAM_FEHLER={type(exc).__name__}: {exc}")
        traceback.print_exc()
        sys.exit(4)

    result("STREAM_LAEUFT")

    sock = getattr(camera, "sock", None)

    if sock is not None:
        result(f"SOCKET_TYPE={type(sock)}")

        for attribute in (
            "addr",
            "camera_id",
            "client_id",
            "data_packets_received",
            "data_bytes_received",
            "acks_received",
            "acks_sent",
        ):
            try:
                value = getattr(sock, attribute)
                result(f"SOCKET_{attribute.upper()}={value}")
            except Exception:
                pass

    result("WARTE_AUF_STREAM")

    for second in range(1, 16):
        time.sleep(1)

        if sock is not None:
            try:
                packets = getattr(sock, "data_packets_received", None)
                bytes_received = getattr(sock, "data_bytes_received", None)

                result(
                    f"STREAM_STATUS={second}s "
                    f"PACKETS={packets} "
                    f"BYTES={bytes_received}"
                )

            except Exception as exc:
                result(f"STREAM_STATUS_FEHLER={type(exc).__name__}: {exc}")

    result("STOP_STREAM")

    try:
        camera.stop_stream("mainStream")
        result("STOP_STREAM_OK")

    except Exception as exc:
        result(f"STOP_STREAM_FEHLER={type(exc).__name__}: {exc}")

except Exception as exc:
    result(f"TEST_FEHLER={type(exc).__name__}: {exc}")
    traceback.print_exc()

finally:
    if camera is not None:
        try:
            camera.close()
            result("CLOSE_OK")
        except Exception as exc:
            result(f"CLOSE_FEHLER={type(exc).__name__}: {exc}")

result("TEST_ENDE")
result("PYTHON_ENDE")
