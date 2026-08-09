"""Reolink P2P API client using the live stream instead of Snapshot."""

from __future__ import annotations

import logging
import shutil
import subprocess
import threading
from datetime import datetime
from typing import Any

from pyneolink import Camera
from pyneolink.core.bc import InvalidMagicError

_LOGGER = logging.getLogger(__name__)


class ReolinkCloudApi:
    """Client for a Reolink camera using P2P."""

    def __init__(
        self,
        uid: str,
        username: str,
        password: str,
    ) -> None:
        """Initialize the P2P client."""

        self._uid = uid
        self._username = username
        self._password = password
        self._lock = threading.Lock()

        self._ffmpeg = shutil.which("ffmpeg")

        if not self._ffmpeg:
            _LOGGER.error(
                "FFmpeg was not found in PATH. "
                "Live-stream snapshots cannot be created."
            )

    @property
    def uid(self) -> str:
        """Return the camera UID."""

        return self._uid

    @staticmethod
    def _timestamp() -> str:
        """Return timestamp for diagnostic logging."""

        return datetime.now().strftime("%H:%M:%S.%f")[:-3]

    @staticmethod
    def _is_jpeg(data: bytes) -> bool:
        """Return True when data contains a JPEG."""

        return (
            len(data) >= 4
            and data[:2] == b"\xff\xd8"
            and data[-2:] == b"\xff\xd9"
        )

    def _create_camera(self) -> Camera:
        """Create a new P2P camera connection."""

        return Camera(
            uuid=self._uid,
            username=self._username,
            password=self._password,
            timeout=30,
            debug=True,
        )

    def connect(self) -> dict[str, Any]:
        """Test P2P connectivity."""

        with self._lock:
            camera = self._create_camera()

            try:
                _LOGGER.info(
                    "[%s] Connecting to Reolink camera %s using P2P",
                    self._timestamp(),
                    self._uid,
                )

                camera.connect()

                _LOGGER.info(
                    "[%s] Successfully connected to Reolink camera %s via P2P",
                    self._timestamp(),
                    self._uid,
                )

                return {
                    "connected": True,
                    "uid": self._uid,
                }

            finally:
                try:
                    camera.close()
                except Exception:
                    _LOGGER.debug(
                        "[%s] Error closing P2P connection",
                        self._timestamp(),
                        exc_info=True,
                    )

    def _stream_snapshot_once(self) -> bytes:
        """
        Get a JPEG frame from the live P2P stream.

        IMPORTANT:
        Do NOT use camera.snapshot().
        The Snapshot command is unreliable with this camera.
        """

        if not self._ffmpeg:
            raise RuntimeError(
                "FFmpeg is required for live-stream snapshots"
            )

        camera = self._create_camera()

        try:
            _LOGGER.info(
                "[%s] Connecting to live stream for %s",
                self._timestamp(),
                self._uid,
            )

            camera.connect()

            _LOGGER.info(
                "[%s] Starting live stream for %s",
                self._timestamp(),
                self._uid,
            )

            # PyNeolink's record() path uses the live MPEG-TS stream.
            #
            # We let ffmpeg read the MPEG-TS stream and extract
            # exactly one JPEG frame.
            #
            # The stream itself is handled by PyNeolink.
            #
            # This section intentionally avoids camera.snapshot().

            process = subprocess.Popen(
                [
                    self._ffmpeg,
                    "-hide_banner",
                    "-loglevel",
                    "error",
                    "-f",
                    "mpegts",
                    "-i",
                    "pipe:0",
                    "-frames:v",
                    "1",
                    "-f",
                    "image2",
                    "-vcodec",
                    "mjpeg",
                    "pipe:1",
                ],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            try:
                # The actual live-stream reader is provided by
                # PyNeolink's media layer.
                #
                # We intentionally don't call camera.snapshot().
                #
                # The stream API differs between PyNeolink releases,
                # therefore the stream object is detected dynamically.

                stream_method = getattr(camera, "stream", None)

                if stream_method is None:
                    raise RuntimeError(
                        "Installed PyNeolink version does not expose "
                        "the live stream API."
                    )

                stream = stream_method(
                    stream="mainStream",
                    quality="high",
                )

                for chunk in stream:
                    if not chunk:
                        continue

                    process.stdin.write(chunk)
                    process.stdin.flush()

                    if process.poll() is not None:
                        break

                try:
                    process.stdin.close()
                except Exception:
                    pass

                jpeg, stderr = process.communicate(timeout=15)

                if process.returncode != 0:
                    error = stderr.decode(
                        "utf-8",
                        errors="replace",
                    ).strip()

                    raise RuntimeError(
                        f"FFmpeg failed with code "
                        f"{process.returncode}: {error}"
                    )

                if not self._is_jpeg(jpeg):
                    raise ValueError(
                        "Live stream did not produce a valid JPEG"
                    )

                _LOGGER.info(
                    "[%s] JPEG frame received from live stream: %d bytes",
                    self._timestamp(),
                    len(jpeg),
                )

                return jpeg

            finally:
                if process.poll() is None:
                    process.kill()

        finally:
            try:
                camera.close()
            except Exception:
                _LOGGER.debug(
                    "[%s] Error closing live-stream connection",
                    self._timestamp(),
                    exc_info=True,
                )

    def snapshot(self) -> bytes:
        """
        Return a JPEG frame.

        This method deliberately does NOT use Reolink's Snapshot command.
        """

        with self._lock:
            try:
                return self._stream_snapshot_once()

            except InvalidMagicError as err:
                _LOGGER.warning(
                    "[%s] Invalid Baichuan packet while reading "
                    "live stream from %s: %s",
                    self._timestamp(),
                    self._uid,
                    err,
                )

                raise

    def close(self) -> None:
        """Close API resources."""

        # Connections are deliberately short-lived.
        return
