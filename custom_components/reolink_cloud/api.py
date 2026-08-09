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

        # One persistent pyneolink connection.
        self._camera: Camera | None = None

        # Protect the socket from concurrent access.
        self._lock = threading.RLock()

    @property
    def uid(self) -> str:
        """Return the camera UID."""

        return self._uid

    @staticmethod
    def _timestamp() -> str:
        """Return a timestamp for diagnostic logging."""

        return datetime.now().strftime("%H:%M:%S.%f")[:-3]

    def _close_locked(self) -> None:
        """Close the current camera connection.

        The caller must hold self._lock.
        """

        camera = self._camera
        self._camera = None

        if camera is None:
            return

        try:
            camera.close()
        except Exception:
            _LOGGER.debug(
                "[%s] Error while closing Reolink P2P connection",
                self._timestamp(),
                exc_info=True,
            )

    def _connect_locked(self) -> None:
        """Create and connect a new camera connection.

        The caller must hold self._lock.
        """

        # Do not create a second connection if one already exists.
        if self._camera is not None:
            return

        _LOGGER.info(
            "[%s] Connecting to Reolink camera %s using P2P",
            self._timestamp(),
            self._uid,
        )

        camera = Camera(
            uuid=self._uid,
            username=self._username,
            password=self._password,
            timeout=30,
            debug=False,
        )

        try:
            camera.connect()

        except Exception:
            _LOGGER.exception(
                "[%s] Failed to connect to Reolink camera %s via P2P",
                self._timestamp(),
                self._uid,
            )

            try:
                camera.close()
            except Exception:
                pass

            raise

        self._camera = camera

        _LOGGER.info(
            "[%s] Successfully connected to Reolink camera %s via P2P",
            self._timestamp(),
            self._uid,
        )

    def connect(self) -> dict[str, Any]:
        """Connect to the camera using Reolink P2P."""

        with self._lock:
            # Keep an existing connection alive.
            if self._camera is None:
                self._connect_locked()

            return {
                "connected": self._camera is not None,
                "uid": self._uid,
            }

    @staticmethod
    def _is_jpeg(data: bytes) -> bool:
        """Return True when data has a JPEG start and end marker."""

        return (
            len(data) >= 4
            and data[:2] == b"\xff\xd8"
            and data[-2:] == b"\xff\xd9"
        )

    def _snapshot_locked(self) -> bytes:
        """Request a snapshot from the current connection.

        The caller must hold self._lock.
        """

        if self._camera is None:
            _LOGGER.info(
                "[%s] No active connection, connecting before snapshot",
                self._timestamp(),
            )

            self._connect_locked()

        camera = self._camera

        if camera is None:
            raise RuntimeError("Camera is not connected")

        _LOGGER.info(
            "[%s] Requesting snapshot from Reolink camera %s",
            self._timestamp(),
            self._uid,
        )

        snapshot = camera.snapshot()

        if not isinstance(snapshot, bytes):
            raise TypeError(
                "Reolink snapshot did not return bytes"
            )

        _LOGGER.info(
            "[%s] Received snapshot from Reolink camera %s: %d bytes",
            self._timestamp(),
            self._uid,
            len(snapshot),
        )

        if not self._is_jpeg(snapshot):
            _LOGGER.error(
                "[%s] Invalid JPEG received from Reolink camera %s: "
                "size=%d header=%s trailer=%s",
                self._timestamp(),
                self._uid,
                len(snapshot),
                snapshot[:16].hex(),
                snapshot[-16:].hex() if snapshot else "",
            )

            raise ValueError(
                "Reolink snapshot is not a valid JPEG"
            )

        return snapshot

    def snapshot(self) -> bytes:
        """Get a snapshot from the camera.

        A failed connection is discarded and recreated once.
        Only one snapshot may access the P2P socket at a time.
        """

        with self._lock:
            try:
                return self._snapshot_locked()

            except Exception as err:
                # Any exception during snapshot can mean that
                # the P2P socket is no longer synchronized.
                _LOGGER.warning(
                    "[%s] Snapshot failed for Reolink camera %s: "
                    "%s: %s",
                    self._timestamp(),
                    self._uid,
                    type(err).__name__,
                    err,
                )

                _LOGGER.info(
                    "[%s] Reconnecting Reolink camera %s "
                    "after snapshot failure",
                    self._timestamp(),
                    self._uid,
                )

                self._close_locked()

                # Reconnect once.
                self._connect_locked()

                _LOGGER.info(
                    "[%s] Retrying snapshot from Reolink camera %s",
                    self._timestamp(),
                    self._uid,
                )

                return self._snapshot_locked()

    def close(self) -> None:
        """Close the P2P connection."""

        with self._lock:
            self._close_locked()
