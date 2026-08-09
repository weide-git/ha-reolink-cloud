import json
import sys
import traceback

print("RESULT: PYTHON_START", flush=True)

try:
    import pyneolink
    from pyneolink.camera import Camera
    print(f"RESULT: PYNEOLINK_VERSION={getattr(pyneolink, '__version__', 'unbekannt')}", flush=True)
    print("RESULT: CAMERA_IMPORT_OK", flush=True)
except Exception as exc:
    print(f"RESULT: IMPORT_FEHLER={type(exc).__name__}: {exc}", flush=True)
    sys.exit(1)

try:
    with open("/data/options.json", "r", encoding="utf-8") as f:
        options = json.load(f)

    uid = options.get("uid", "")
    username = options.get("username", "admin")
    password = options.get("password", "")

    print(f"RESULT: UID={uid}", flush=True)
    print(f"RESULT: USERNAME={username}", flush=True)
    print(f"RESULT: PASSWORD_GESETZT={'JA' if password else 'NEIN'}", flush=True)
    print(f"RESULT: PASSWORD_LAENGE={len(password)}", flush=True)

    camera = Camera(uid=uid, username=username, password=password)
    print("RESULT: CAMERA_ERZEUGT", flush=True)

    print("RESULT: CONNECT_START", flush=True)
    camera.connect()
    print("RESULT: CONNECT_OK", flush=True)

    print("RESULT: LOGIN_START", flush=True)
    camera.login()
    print("RESULT: LOGIN_OK", flush=True)

    print("RESULT: START_STREAM", flush=True)
    camera.start_stream("mainStream")
    print("RESULT: START_STREAM_OK", flush=True)

    print(f"RESULT: SOCKET_TYPE={type(getattr(camera, 'sock', None))}", flush=True)
    print("RESULT: RAW_RECV_START", flush=True)

    messages = 0
    payload_bytes = 0
    raw_errors = 0

    for attempt in range(1, 11):
        print(f"RESULT: RECV_ATTEMPT={attempt}", flush=True)
        try:
            msg = camera._recv(timeout=3.0)
            messages += 1
            print(f"RESULT: RECV_OK={attempt}", flush=True)
            print(f"RESULT: MSG_TYPE={type(msg)}", flush=True)

            header = getattr(msg, "header", None)
            payload = getattr(msg, "payload", b"")

            if header is not None:
                print(f"RESULT: MSG_ID={getattr(header, 'msg_id', None)}", flush=True)
                print(f"RESULT: MSG_NUM={getattr(header, 'msg_num', None)}", flush=True)
                print(f"RESULT: BODY_LEN={getattr(header, 'body_len', None)}", flush=True)
                print(f"RESULT: RESPONSE_CODE={getattr(header, 'response_code', None)}", flush=True)

            if isinstance(payload, (bytes, bytearray)):
                payload_bytes += len(payload)
                print(f"RESULT: PAYLOAD_LEN={len(payload)}", flush=True)
                print(f"RESULT: PAYLOAD_FIRST_32={bytes(payload[:32]).hex()}", flush=True)
                print(f"RESULT: H264_MARKER={'JA' if b'H264' in payload else 'NEIN'}", flush=True)
                print(
                    "RESULT: H264_ANNEXB_STARTCODE="
                    + ("JA" if b"\x00\x00\x00\x01" in payload or b"\x00\x00\x01" in payload else "NEIN"),
                    flush=True,
                )

        except Exception as exc:
            raw_errors += 1
            print(f"RESULT: RECV_FEHLER={type(exc).__name__}: {exc}", flush=True)

            if type(exc).__name__ == "InvalidMagicError":
                print("RESULT: RAW_UDP_DATEN_ERKANNT=JA", flush=True)
            if type(exc).__name__ == "TimeoutError":
                print("RESULT: UDP_TIMEOUT=JA", flush=True)

    print("RESULT: RAW_RECV_ENDE", flush=True)
    print(f"RESULT: MESSAGE_COUNT={messages}", flush=True)
    print(f"RESULT: PAYLOAD_BYTES={payload_bytes}", flush=True)
    print(f"RESULT: RAW_ERRORS={raw_errors}", flush=True)

    print("RESULT: STOP_STREAM", flush=True)
    try:
        camera.stop_stream("mainStream")
        print("RESULT: STOP_STREAM_OK", flush=True)
    except Exception as exc:
        print(f"RESULT: STOP_STREAM_FEHLER={type(exc).__name__}: {exc}", flush=True)

    try:
        camera.close()
        print("RESULT: CLOSE_OK", flush=True)
    except Exception as exc:
        print(f"RESULT: CLOSE_FEHLER={type(exc).__name__}: {exc}", flush=True)

except Exception as exc:
    print(f"RESULT: TEST_FEHLER={type(exc).__name__}: {exc}", flush=True)
    traceback.print_exc()

print("RESULT: TEST_ENDE", flush=True)
print("RESULT: PYTHON_ENDE", flush=True)
