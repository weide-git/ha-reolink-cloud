"""Reolink P2P API client."""

from __future__ import annotations

import logging
import threading
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
        self._camera: Camera | None = None

        # Only allow one camera operation at a time.
        self._snapshot_lock = threading.Lock()

    @property
    def uid(self) -> str:
        """Return the camera UID."""

        return self._uid

    def connect(self) -> dict[str, Any]:
        """Connect to the camera using Reolink P2P."""

        _LOGGER.info(
            "Connecting to Reolink camera %s using P2P",
            self._uid,
        )

        camera = Camera(
            uuid=self._uid,
            username=self._username,
            password=self._password,
            timeout=120,
            debug=True,
        )

        camera.connect()

        self._camera = camera

        _LOGGER.info(
            "Successfully connected to Reolink camera %s via P2P",
            self._uid,
        )

        return {
            "connected": True,
            "uid": self._uid,
        }

    def snapshot(self) -> bytes:
        """Get a snapshot from the camera."""

        if self._camera is None:
            raise RuntimeError("Camera is not connected")

        # Prevent Home Assistant from starting several snapshot
        # requests against the same P2P connection at once.
        if not self._snapshot_lock.acquire(blocking=False):
            _LOGGER.warning(
                "Snapshot request ignored because another snapshot "
                "is already in progress for Reolink camera %s",
                self._uid,
            )
            raise RuntimeError(
                "Another snapshot request is already in progress"
            )

        try:
            _LOGGER.info(
                "Requesting snapshot from Reolink camera %s",
                self._uid,
            )

            snapshot = self._camera.snapshot()

            _LOGGER.info(
                "Camera.snapshot() returned for Reolink camera %s",
                self._uid,
            )

            _LOGGER.info(
                "Snapshot return type: %s",
                type(snapshot).__name__,
            )

            if isinstance(snapshot, bytes):
                _LOGGER.info(
                    "Received snapshot from Reolink camera %s "
                    "(%d bytes)",
                    self._uid,
                    len(snapshot),
                )

                if snapshot.startswith(b"\xff\xd8\xff"):
                    _LOGGER.info(
                        "Snapshot starts with valid JPEG signature"
                    )
                else:
                    _LOGGER.warning(
                        "Snapshot does not start with a JPEG signature. "
                        "First 16 bytes: %s",
                        snapshot[:16].hex(" "),
                    )

                return snapshot

            raise TypeError(
                "Reolink snapshot did not return bytes; "
                f"got {type(snapshot).__name__}"
            )

        except Exception:
            _LOGGER.exception(
                "Error while requesting snapshot from "
                "Reolink camera %s",
                self._uid,
            )
            raise

        finally:
            self._snapshot_lock.release()

    def close(self) -> None:
        """Close the P2P connection."""

        if self._camera is not None:
            try:
                self._camera.close()
            except Exception:
                _LOGGER.exception(
                    "Error while closing Reolink P2P connection"
                )
            finally:
                self._camera = None
