import json
import sys
import traceback

print("RESULT: PYTHON_START", flush=True)

camera = None

# ------------------------------------------------------------
# PyNeolink importieren
# ------------------------------------------------------------
try:
    import pyneolink
    from pyneolink.camera import Camera

    version = getattr(pyneolink, "__version__", "unbekannt")

    print(f"RESULT: PYNEOLINK_VERSION={version}", flush=True)
    print("RESULT: CAMERA_IMPORT_OK", flush=True)

except Exception as exc:
    print(
        f"RESULT: IMPORT_FEHLER={type(exc).__name__}: {exc}",
        flush=True,
    )
    traceback.print_exc()
    print("RESULT: TEST_ENDE", flush=True)
    sys.exit(1)


# ------------------------------------------------------------
# Optionen lesen
# ------------------------------------------------------------
try:
    with open("/data/options.json", "r", encoding="utf-8") as f:
        options = json.load(f)

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

except Exception as exc:
    print(
        f"RESULT: OPTIONS_FEHLER={type(exc).__name__}: {exc}",
        flush=True,
    )
    traceback.print_exc()
    print("RESULT: TEST_ENDE", flush=True)
    sys.exit(1)


# ------------------------------------------------------------
# Kameraobjekt erzeugen
# ------------------------------------------------------------
try:
    camera = Camera(
        uid=uid,
        username=username,
        password=password,
        debug=True,
    )

    print("RESULT: CAMERA_ERZEUGT", flush=True)

except Exception as exc:
    print(
        f"RESULT: CAMERA_ERZEUGT_FEHLER={type(exc).__name__}: {exc}",
        flush=True,
    )
    traceback.print_exc()
    print("RESULT: TEST_ENDE", flush=True)
    sys.exit(1)


# ------------------------------------------------------------
# Verbindung
# ------------------------------------------------------------
try:
    print("RESULT: CONNECT_START", flush=True)

    camera.connect()

    print("RESULT: CONNECT_OK", flush=True)

except Exception as exc:
    print(
        f"RESULT: CONNECT_FEHLER={type(exc).__name__}: {exc}",
        flush=True,
    )

    traceback.print_exc()

    # Wichtig:
    # Bei dem bisherigen Fehler
    #
    #   Reolink register did not return connection details
    #
    # wollen wir NICHT so tun, als wäre die Kamera verbunden.
    if type(exc).__name__ == "TimeoutError":
        print("RESULT: CONNECT_TIMEOUT=JA", flush=True)

    print("RESULT: CONNECT_NICHT_ERFOLGREICH", flush=True)

    try:
        if camera is not None:
            camera.close()
            print("RESULT: CLOSE_OK", flush=True)
    except Exception as close_exc:
        print(
            f"RESULT: CLOSE_FEHLER={type(close_exc).__name__}: {close_exc}",
            flush=True,
        )

    print("RESULT: TEST_ENDE", flush=True)
    print("RESULT: PYTHON_ENDE", flush=True)

    # Anwendung erfolgreich beenden, damit der Add-on-Container
    # nicht ständig neu gestartet wird.
    sys.exit(0)


# ------------------------------------------------------------
# Verbindung erfolgreich
# ------------------------------------------------------------
print("RESULT: CONNECTION_ESTABLISHED", flush=True)

try:
    sock = getattr(camera, "sock", None)

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

except Exception as exc:
    print(
        f"RESULT: SOCKET_INFO_FEHLER={type(exc).__name__}: {exc}",
        flush=True,
    )


# ------------------------------------------------------------
# Login
# ------------------------------------------------------------
try:
    print("RESULT: LOGIN_START", flush=True)

    camera.login()

    print("RESULT: LOGIN_OK", flush=True)

except Exception as exc:
    print(
        f"RESULT: LOGIN_FEHLER={type(exc).__name__}: {exc}",
        flush=True,
    )

    traceback.print_exc()

    try:
        camera.close()
        print("RESULT: CLOSE_OK", flush=True)
    except Exception as close_exc:
        print(
            f"RESULT: CLOSE_FEHLER={type(close_exc).__name__}: {close_exc}",
            flush=True,
        )

    print("RESULT: TEST_ENDE", flush=True)
    print("RESULT: PYTHON_ENDE", flush=True)
    sys.exit(0)


# ------------------------------------------------------------
# Stream starten
# ------------------------------------------------------------
stream_started = False

try:
    print("RESULT: START_STREAM", flush=True)

    camera.start_stream("mainStream")

    stream_started = True

    print("RESULT: START_STREAM_OK", flush=True)

except Exception as exc:
    print(
        f"RESULT: START_STREAM_FEHLER={type(exc).__name__}: {exc}",
        flush=True,
    )
    traceback.print_exc()


# ------------------------------------------------------------
# Raw UDP Empfang testen
# ------------------------------------------------------------
if stream_started:

    print("RESULT: RAW_RECV_START", flush=True)

    messages = 0
    payload_bytes = 0
    raw_errors = 0

    for attempt in range(1, 11):

        print(
            f"RESULT: RECV_ATTEMPT={attempt}",
            flush=True,
        )

        try:
            msg = camera._recv(timeout=3.0)

            messages += 1

            print(
                f"RESULT: RECV_OK={attempt}",
                flush=True,
            )

            print(
                f"RESULT: MSG_TYPE={type(msg)}",
                flush=True,
            )

            header = getattr(msg, "header", None)
            payload = getattr(msg, "payload", b"")

            if header is not None:

                print(
                    f"RESULT: MSG_ID={getattr(header, 'msg_id', None)}",
                    flush=True,
                )

                print(
                    f"RESULT: MSG_NUM={getattr(header, 'msg_num', None)}",
                    flush=True,
                )

                print(
                    f"RESULT: BODY_LEN={getattr(header, 'body_len', None)}",
                    flush=True,
                )

                print(
                    f"RESULT: RESPONSE_CODE={getattr(header, 'response_code', None)}",
                    flush=True,
                )

            if isinstance(payload, (bytes, bytearray)):

                payload_bytes += len(payload)

                print(
                    f"RESULT: PAYLOAD_LEN={len(payload)}",
                    flush=True,
                )

                print(
                    f"RESULT: PAYLOAD_FIRST_32={bytes(payload[:32]).hex()}",
                    flush=True,
                )

                if b"H264" in payload:
                    print(
                        "RESULT: H264_MARKER=JA",
                        flush=True,
                    )
                else:
                    print(
                        "RESULT: H264_MARKER=NEIN",
                        flush=True,
                    )

                annexb = (
                    b"\x00\x00\x00\x01" in payload
                    or b"\x00\x00\x01" in payload
                )

                print(
                    "RESULT: H264_ANNEXB_STARTCODE="
                    + ("JA" if annexb else "NEIN"),
                    flush=True,
                )

        except Exception as exc:

            raw_errors += 1

            print(
                f"RESULT: RECV_FEHLER={type(exc).__name__}: {exc}",
                flush=True,
            )

            if type(exc).__name__ == "InvalidMagicError":
                print(
                    "RESULT: RAW_UDP_DATEN_ERKANNT=JA",
                    flush=True,
                )

            if type(exc).__name__ == "TimeoutError":
                print(
                    "RESULT: UDP_TIMEOUT=JA",
                    flush=True,
                )

    print("RESULT: RAW_RECV_ENDE", flush=True)

    print(
        f"RESULT: MESSAGE_COUNT={messages}",
        flush=True,
    )

    print(
        f"RESULT: PAYLOAD_BYTES={payload_bytes}",
        flush=True,
    )

    print(
        f"RESULT: RAW_ERRORS={raw_errors}",
        flush=True,
    )

else:
    print(
        "RESULT: RAW_RECV_UEBERSPRUNGEN=JA",
        flush=True,
    )


# ------------------------------------------------------------
# Stream stoppen
# ------------------------------------------------------------
if stream_started:

    print("RESULT: STOP_STREAM", flush=True)

    try:
        camera.stop_stream("mainStream")

        print(
            "RESULT: STOP_STREAM_OK",
            flush=True,
        )

    except Exception as exc:
        print(
            f"RESULT: STOP_STREAM_FEHLER={type(exc).__name__}: {exc}",
            flush=True,
        )


# ------------------------------------------------------------
# Verbindung schließen
# ------------------------------------------------------------
try:
    camera.close()

    print(
        "RESULT: CLOSE_OK",
        flush=True,
    )

except Exception as exc:
    print(
        f"RESULT: CLOSE_FEHLER={type(exc).__name__}: {exc}",
        flush=True,
    )


print("RESULT: TEST_ENDE", flush=True)
print("RESULT: PYTHON_ENDE", flush=True)
