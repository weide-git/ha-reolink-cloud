#!/bin/sh

set -eu

echo "========================================"
echo " Reolink PyNeolink Camera/Media API"
echo "========================================"
echo

python - <<'PY'
import inspect

print("RESULT: CAMERA_BEGIN")

try:
    import pyneolink.camera as camera

    print("RESULT: CAMERA_FILE=" + str(camera.__file__))

    for name, obj in inspect.getmembers(camera):
        if inspect.isclass(obj) or inspect.isfunction(obj):
            print("RESULT: CAMERA_OBJECT=" + name)

            try:
                print(
                    "RESULT: CAMERA_SIGNATURE="
                    + name
                    + "="
                    + str(inspect.signature(obj))
                )
            except Exception:
                pass

except Exception as e:
    print("RESULT: CAMERA_ERROR=" + repr(e))

print("RESULT: CAMERA_END")
print()

print("RESULT: MEDIA_BEGIN")

try:
    import pyneolink.core.media as media

    print("RESULT: MEDIA_FILE=" + str(media.__file__))

    for name, obj in inspect.getmembers(media):
        if inspect.isclass(obj) or inspect.isfunction(obj):
            print("RESULT: MEDIA_OBJECT=" + name)

            try:
                print(
                    "RESULT: MEDIA_SIGNATURE="
                    + name
                    + "="
                    + str(inspect.signature(obj))
                )
            except Exception:
                pass

except Exception as e:
    print("RESULT: MEDIA_ERROR=" + repr(e))

print("RESULT: MEDIA_END")
print()

print("RESULT: STREAM_SERVER_BEGIN")

try:
    import pyneolink.stream_server as ss

    print("RESULT: STREAM_SERVER_FILE=" + str(ss.__file__))

    for name, obj in inspect.getmembers(ss):
        if inspect.isclass(obj) or inspect.isfunction(obj):
            print("RESULT: STREAM_OBJECT=" + name)

            try:
                print(
                    "RESULT: STREAM_SIGNATURE="
                    + name
                    + "="
                    + str(inspect.signature(obj))
                )
            except Exception:
                pass

except Exception as e:
    print("RESULT: STREAM_ERROR=" + repr(e))

print("RESULT: STREAM_SERVER_END")
print()
print("RESULT: DIAGNOSE_END")
PY
