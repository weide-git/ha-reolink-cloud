"""Reolink P2P API client."""

from __future__ import annotations

import logging
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
