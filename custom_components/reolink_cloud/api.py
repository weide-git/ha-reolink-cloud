"""Reolink P2P API client."""

from **future** import annotations

import logging
import threading
from datetime import datetime
from typing import Any

from pyneolink import Camera

_LOGGER = logging.getLogger(**name**)

class ReolinkCloudApi:
"""Client for a Reolink camera using P2P."""

```
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
    self._camera: Camera | None = None

    # pyneolink uses a single socket per Camera instance.
    # Access to that instance must therefore be serialized.
    self._lock = threading.RLock()

@property
def uid(self) -> str:
    """Return the camera UID."""

    return self._uid

def _log_time(self) -> str:
    """Return the current local time for diagnostic logging."""

    return datetime.now().strftime("%H:%M:%S.%f")[:-3]

def _connect_locked(self) -> None:
    """Connect to the camera.

    The caller must hold self._lock.
    """

    _LOGGER.info(
        "[%s] Connecting to Reolink camera %s using P2P",
        self._log_time(),
        self._uid,
    )

    camera = Camera(
        uuid=self._uid,
        username=self._username,
        password=self._password,
        timeout=120,
        debug=True,
    )

    try:
        camera.connect()
    except Exception:
        _LOGGER.exception(
            "[%s] Failed to connect to Reolink camera %s via P2P",
            self._log_time(),
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
        self._log_time(),
        self._uid,
    )

def connect(self) -> dict[str, Any]:
    """Connect to the camera using Reolink P2P."""

    with self._lock:
        # Close an existing connection before creating a new one.
        if self._camera is not None:
            _LOGGER.info(
                "[%s] Closing existing Reolink connection before reconnect",
                self._log_time(),
            )

            try:
                self._camera.close()
            except Exception:
                _LOGGER.exception(
                    "[%s] Error while closing existing Reolink connection",
                    self._log_time(),
                )
            finally:
                self._camera = None

        self._connect_locked()

        return {
            "connected": True,
            "uid": self._uid,
        }

def _close_locked(self) -> None:
    """Close the current camera connection.

    The caller must hold self._lock.
    """

    if self._camera is None:
        return

    camera = self._camera
    self._camera = None

    try:
        camera.close()
    except Exception:
        _LOGGER.exception(
            "[%s] Error while closing Reolink P2P connection",
            self._log_time(),
        )

def _is_jpeg(self, data: bytes) -> bool:
    """Check whether the returned data looks like a JPEG."""

    if len(data) < 4:
        return False

    return data[:2] == b"\xff\xd8" and data[-2:] == b"\xff\xd9"

def _snapshot_locked(self) -> bytes:
    """Request a snapshot.

    The caller must hold self._lock.
    """

    if self._camera is None:
        _LOGGER.info(
            "[%s] No active Reolink connection, connecting before snapshot",
            self._log_time(),
        )

        self._connect_locked()

    if self._camera is None:
        raise RuntimeError("Camera is not connected")

    _LOGGER.info(
        "[%s] Requesting snapshot from Reolink camera %s",
        self._log_time(),
        self._uid,
    )

    snapshot = self._camera.snapshot()

    if not isinstance(snapshot, bytes):
        raise TypeError(
            "Reolink snapshot did not return bytes"
        )

    _LOGGER.info(
        "[%s] Received snapshot from Reolink camera %s: %d bytes",
        self._log_time(),
        self._uid,
        len(snapshot),
    )

    if len(snapshot) >= 2:
        _LOGGER.debug(
            "[%s] Snapshot header=%s trailer=%s",
            self._log_time(),
            snapshot[:2].hex(),
            snapshot[-2:].hex(),
        )

    if not self._is_jpeg(snapshot):
        _LOGGER.error(
            "[%s] Reolink snapshot is not a valid JPEG: "
            "size=%d header=%s trailer=%s",
            self._log_time(),
            len(snapshot),
            snapshot[:16].hex(),
            snapshot[-16:].hex() if snapshot else "",
        )

        raise ValueError(
            "Reolink snapshot is not a valid JPEG"
        )

    _LOGGER.info(
        "[%s] Valid JPEG received from Reolink camera %s (%d bytes)",
        self._log_time(),
        self._uid,
        len(snapshot),
    )

    return snapshot

def snapshot(self) -> bytes:
    """Get a snapshot from the camera.

    If the existing pyneolink connection has become invalid,
    reconnect once and retry the snapshot.
    """

    with self._lock:
        try:
            return self._snapshot_locked()

        except (OSError, RuntimeError) as err:
            _LOGGER.warning(
                "[%s] Reolink snapshot failed: %s: %s",
                self._log_time(),
                type(err).__name__,
                err,
            )

            _LOGGER.info(
                "[%s] Reconnecting Reolink camera %s after snapshot failure",
                self._log_time(),
                self._uid,
            )

            self._close_locked()

            # Reconnect and retry exactly once.
            self._connect_locked()

            _LOGGER.info(
                "[%s] Retrying snapshot from Reolink camera %s",
                self._log_time(),
                self._uid,
            )

            return self._snapshot_locked()

def close(self) -> None:
    """Close the P2P connection."""

    with self._lock:
        self._close_locked()
