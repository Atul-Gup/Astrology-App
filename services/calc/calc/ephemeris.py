"""Local JPL ephemeris loading. No network access: the kernel file must already exist.

The kernel is fetched once by hand with scripts/fetch_ephemeris.py; this module never downloads.
"""

import os
from datetime import UTC, datetime
from functools import lru_cache
from pathlib import Path

from skyfield.api import Loader
from skyfield.jpllib import SpiceKernel

KERNEL_FILENAME = "de440s.bsp"
KERNEL_PATH_ENV = "CALC_EPHEMERIS_PATH"

# Bodies exposed so far. Planets are added in T4 once the body handling is decided.
_SUPPORTED_BODIES = {"sun", "moon"}


class EphemerisNotFoundError(Exception):
    """The ephemeris kernel file is missing."""


class DateOutOfRangeError(ValueError):
    """The requested date is outside the range covered by the kernel."""


def default_kernel_path() -> Path:
    override = os.environ.get(KERNEL_PATH_ENV)
    if override:
        return Path(override)
    return Path(__file__).resolve().parent.parent / "data" / "ephemeris" / KERNEL_FILENAME


class Ephemeris:
    def __init__(self, path: Path, kernel: SpiceKernel, ts) -> None:
        self.path = path
        self._kernel = kernel
        self._ts = ts
        segments = kernel.spk.segments
        # Conservative range: the span covered by every segment in the kernel.
        self.start = ts.tdb_jd(max(s.start_jd for s in segments)).utc_datetime()
        self.end = ts.tdb_jd(min(s.end_jd for s in segments)).utc_datetime()

    @property
    def kernel_name(self) -> str:
        return self.path.name

    def geocentric_position_au(self, body: str, when: datetime) -> tuple[float, float, float]:
        """Geometric geocentric ICRF position in AU. Not yet corrected for light time etc."""
        if body not in _SUPPORTED_BODIES:
            raise ValueError(f"Unknown body {body!r}; supported: {sorted(_SUPPORTED_BODIES)}")
        if when.tzinfo is None:
            raise ValueError("datetime must be timezone-aware (UTC)")
        when = when.astimezone(UTC)
        if not self.start <= when <= self.end:
            raise DateOutOfRangeError(
                f"{when.isoformat()} is outside the ephemeris range "
                f"{self.start.date()} to {self.end.date()} ({self.kernel_name})"
            )
        t = self._ts.from_datetime(when)
        x, y, z = (self._kernel[body] - self._kernel["earth"]).at(t).position.au
        return float(x), float(y), float(z)


def load_ephemeris(path: Path) -> Ephemeris:
    path = Path(path)
    if not path.is_file():
        raise EphemerisNotFoundError(
            f"Ephemeris kernel not found at {path}. "
            "Run scripts/fetch_ephemeris.py once to download it; "
            "the service never downloads at runtime."
        )
    # Loader(...).timescale() uses Skyfield's built-in leap-second data (no download).
    ts = Loader(str(path.parent), verbose=False).timescale()
    return Ephemeris(path, SpiceKernel(str(path)), ts)


@lru_cache(maxsize=1)
def get_ephemeris() -> Ephemeris:
    """The single shared instance, loaded on first use (and at startup by the app)."""
    return load_ephemeris(default_kernel_path())
