"""Local birth date/time + IANA timezone name -> UTC, using the IANA tz database (via tzdata).

Historical offsets come from the tz database, so results depend on the installed tzdata version.
Local times that do not exist (clock-forward gap) or occur twice (clock-back overlap) are
rejected rather than guessed: choosing one occurrence would be a hidden convention.
"""

import math
from dataclasses import dataclass
from datetime import UTC, date, datetime, time, timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


class InvalidTimezoneError(ValueError):
    """The timezone name is not a known IANA zone."""


class NonexistentLocalTimeError(ValueError):
    """The local time falls in a clock-forward gap and never happened."""


class AmbiguousLocalTimeError(ValueError):
    """The local time falls in a clock-back overlap and happened twice."""


class InvalidCoordinatesError(ValueError):
    """Latitude or longitude is missing, non-finite, or out of range."""


@dataclass(frozen=True)
class LocalMoment:
    utc: datetime  # timezone-aware, UTC
    local: datetime  # timezone-aware, in the zone named by tz_name
    tz_name: str
    utc_offset: timedelta  # offset applied at this moment


def _zone(tz_name: str) -> ZoneInfo:
    try:
        return ZoneInfo(tz_name)
    except (ZoneInfoNotFoundError, ValueError, OSError) as exc:
        raise InvalidTimezoneError(f"Unknown timezone name: {tz_name!r}") from exc


def local_to_utc(birth_date: date, birth_time: time, tz_name: str) -> LocalMoment:
    if birth_time.tzinfo is not None:
        raise ValueError("birth_time must be naive local time; give the zone as tz_name")
    zone = _zone(tz_name)
    naive = datetime.combine(birth_date, birth_time)

    first = naive.replace(tzinfo=zone, fold=0)
    second = naive.replace(tzinfo=zone, fold=1)

    def round_trips(moment: datetime) -> bool:
        return moment.astimezone(UTC).astimezone(zone).replace(tzinfo=None) == naive

    label = f"{naive.isoformat(sep=' ')} in {tz_name}"
    if not (round_trips(first) and round_trips(second)):
        raise NonexistentLocalTimeError(
            f"{label} does not exist (clock change skips it); ask for a different time"
        )
    if first.utcoffset() != second.utcoffset():
        raise AmbiguousLocalTimeError(
            f"{label} is ambiguous (clock change repeats it, offsets "
            f"{first.utcoffset()} and {second.utcoffset()}); ask which one applies"
        )

    return LocalMoment(
        utc=first.astimezone(UTC),
        local=first,
        tz_name=tz_name,
        utc_offset=first.utcoffset(),
    )


def validate_coordinates(latitude: float, longitude: float) -> None:
    for name, value, limit in (("latitude", latitude, 90), ("longitude", longitude, 180)):
        if not math.isfinite(value) or abs(value) > limit:
            raise InvalidCoordinatesError(f"{name} must be between -{limit} and {limit}: {value}")
