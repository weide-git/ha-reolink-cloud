import os
import sys
import time

print("RESULT: PYTHON_START", flush=True)

try:
    import pyneolink
    from pyneolink.camera import Camera

    print(f"RESULT: PYNEOLINK_VERSION={getattr(pyneolink, '__version__', 'unknown')}", flush=True)
    print("RESULT: CAMERA_IMPORT_OK", flush=True)

except Exception as exc:
    print(f"RESULT: IMPORT_FEHLER={type(exc).__name__}: {exc}", flush=True)
    sys.exit(1)


uid = os.environ.get("REOLINK_UID", "")
username = os.environ.get("REOLINK_USERNAME", "admin")
password = os.environ.get("REOLINK_PASSWORD", "")

print(f"RESULT: UID={uid}", flush=True)
print(f"RESULT: USERNAME={username}", flush=True)
print(f"RESULT: PASSWORD_GESETZT={'JA' if password else 'NEIN'}", flush=True)
print(f"RESULT: PASSWORD_LAENGE={len(password)}", flush=True)

if not uid:
    print("RESULT: FEHLER=UID_FEHLT", flush=True)
    sys.exit(1)

try:
    print("RESULT: CAMERA_ERZEUGT", flush=True)

    camera = Camera(
        uid=uid,
        username=username,
        password=password,
    )

    print("RESULT: CAMERA_OBJEKT_OK", flush=True)

    print("RESULT: CONNECT_START", flush=True)
    camera.connect()
    print("RESULT: CONNECT_OK", flush=True)

    print("RESULT: LOGIN_START", flush=True)
    login_result = camera.login()
    print("RESULT: LOGIN_OK", flush=True)
    print(f"RESULT: LOGIN_RESULT_TYP={type(login_result)}", flush=True)

    print("RESULT: START_STREAM", flush=True)
    camera.start_stream("mainStream")
    print("RESULT: START_STREAM_OK", flush=True)

    sock = getattr(camera, "sock", None)

    print(f"RESULT: SOCKET_TYP={type(sock)}", flush=True)

    if sock is None:
        print("RESULT: FEHLER=KEIN_SOCKET", flush=True)
    else:
        print("RESULT: RAW_RECV_START", flush=True)

        packets = 0
        total_bytes = 0
        start = time.time()

        while time.time() - start < 15:
            try:
                msg = camera._recv(timeout=2.0)

                packets += 1

                payload = getattr(msg, "payload", b"")
                if payload is None:
                    payload = b""

                total_bytes += len(payload)

                print(
                    f"RESULT: PACKET={packets} "
                    f"MSG_ID={getattr(msg.header, 'msg_id', '?')} "
                    f"MSG_NUM={getattr(msg.header, 'msg_num', '?')} "
                    f"PAYLOAD={len(payload)} "
                    f"TOTAL={total_bytes}",
                    flush=True,
                )

                if payload:
                    print(
                        "RESULT: FIRST_BYTES="
                        + payload[:32].hex(),
                        flush=True,
                    )

            except Exception as exc:
                print(
                    f"RESULT: RECV_FEHLER={type(exc).__name__}: {exc}",
                    flush=True,
                )

                # Bei Timeout weiter testen
                if "Timeout" in type(exc).__name__:
                    continue

                break

        print(f"RESULT: PACKETS={packets}", flush=True)
        print(f"RESULT: BYTES={total_bytes}", flush=True)

    print("RESULT: STOP_STREAM", flush=True)

    try:
        camera.stop_stream("mainStream")
        print("RESULT: STOP_STREAM_OK", flush=True)
    except Exception as exc:
        print(
            f"RESULT: STOP_STREAM_FEHLER={type(exc).__name__}: {exc}",
            flush=True,
        )

    try:
        camera.close()
        print("RESULT: CLOSE_OK", flush=True)
    except Exception as exc:
        print(
            f"RESULT: CLOSE_FEHLER={type(exc).__name__}: {exc}",
            flush=True,
        )

except Exception as exc:
    print(
        f"RESULT: HAUPTFEHLER={type(exc).__name__}: {exc}",
        flush=True,
    )

    try:
        camera.close()
    except Exception:
        pass

    sys.exit(1)

print("RESULT: TEST_ENDE", flush=True)
sys.exit(0)
