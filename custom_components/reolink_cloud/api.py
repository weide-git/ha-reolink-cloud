"""Reolink P2P API client."""

from __future__ import annotations

import logging
import threading
from datetime import datetime
from typing import Any

from pyneolink import Camera

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

        # Only one complete P2P transaction at a time.
        self._lock = threading.Lock()

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
        """Return True when data has JPEG start/end markers."""
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
            timeout=120,
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
                    "[%s] Successfully connected to Reolink camera %s",
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
                    _LOGGER.exception(
                        "[%s] Error closing P2P connection",
                        self._timestamp(),
                    )

    def snapshot(self) -> bytes:
        """Get a snapshot using a fresh P2P connection."""

        with self._lock:
            camera = self._create_camera()

            try:
                _LOGGER.info(
                    "[%s] Connecting for snapshot: %s",
                    self._timestamp(),
                    self._uid,
                )

                camera.connect()

                _LOGGER.info(
                    "[%s] Requesting snapshot from %s",
                    self._timestamp(),
                    self._uid,
                )

                snapshot = camera.snapshot()

                if not isinstance(snapshot, bytes):
                    raise TypeError(
                        "Reolink snapshot did not return bytes"
                    )

                _LOGGER.info(
                    "[%s] Snapshot received: %d bytes",
                    self._timestamp(),
                    len(snapshot),
                )

                if not self._is_jpeg(snapshot):
                    _LOGGER.error(
                        "[%s] Invalid JPEG: size=%d header=%s trailer=%s",
                        self._timestamp(),
                        len(snapshot),
                        snapshot[:16].hex(),
                        snapshot[-16:].hex(),
                    )

                    raise ValueError(
                        "Reolink snapshot is not a valid JPEG"
                    )

                return snapshot

            finally:
                try:
                    camera.close()
                except Exception:
                    _LOGGER.exception(
                        "[%s] Error closing snapshot connection",
                        self._timestamp(),
                    )

    def close(self) -> None:
        """Close connection.

        Connections are deliberately short-lived, so there is
        nothing persistent to close here.
        """
