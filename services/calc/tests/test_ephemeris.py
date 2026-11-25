import math
import socket
from datetime import UTC, datetime, timedelta

import pytest

from calc.ephemeris import (
    DateOutOfRangeError,
    Ephemeris,
    EphemerisNotFoundError,
    default_kernel_path,
    get_ephemeris,
    load_ephemeris,
)

KERNEL_HELP = "run scripts/fetch_ephemeris.py"


@pytest.fixture(scope="module")
def eph() -> Ephemeris:
    if not default_kernel_path().exists():
        pytest.fail(f"Ephemeris kernel missing: {KERNEL_HELP}")
    return get_ephemeris()


def test_range_covers_1900_to_2100(eph):
    assert eph.start <= datetime(1900, 1, 1, tzinfo=UTC)
    assert eph.end >= datetime(2100, 12, 31, tzinfo=UTC)


def test_range_is_utc_aware(eph):
    assert eph.start.tzinfo is not None
    assert eph.end.tzinfo is not None


def test_position_is_finite_and_plausible(eph):
    when = datetime(2000, 1, 1, 12, tzinfo=UTC)
    sun = eph.geocentric_position_au("sun", when)
    moon = eph.geocentric_position_au("moon", when)
    assert all(math.isfinite(c) for c in (*sun, *moon))
    sun_dist = math.sqrt(sum(c * c for c in sun))
    moon_dist = math.sqrt(sum(c * c for c in moon))
    assert 0.98 < sun_dist < 1.02  # Sun is about 1 AU away
    assert 0.0023 < moon_dist < 0.0028  # Moon is about 0.00257 AU away


def test_date_before_range_raises_clear_error(eph):
    with pytest.raises(DateOutOfRangeError) as exc:
        eph.geocentric_position_au("sun", eph.start - timedelta(days=1))
    assert str(eph.start.date()) in str(exc.value)
    assert str(eph.end.date()) in str(exc.value)


def test_date_after_range_raises_clear_error(eph):
    with pytest.raises(DateOutOfRangeError):
        eph.geocentric_position_au("sun", eph.end + timedelta(days=1))


def test_dates_just_inside_range_work(eph):
    eph.geocentric_position_au("sun", eph.start + timedelta(days=1))
    eph.geocentric_position_au("sun", eph.end - timedelta(days=1))


def test_naive_datetime_is_rejected(eph):
    with pytest.raises(ValueError, match="timezone"):
        eph.geocentric_position_au("sun", datetime(2000, 1, 1, 12))


def test_unknown_body_is_rejected(eph):
    with pytest.raises(ValueError, match="body"):
        eph.geocentric_position_au("pluto-ish", datetime(2000, 1, 1, tzinfo=UTC))


def test_missing_kernel_raises_and_does_not_download(tmp_path, monkeypatch):
    def no_network(*args, **kwargs):
        raise AssertionError("network access attempted")

    monkeypatch.setattr(socket.socket, "connect", no_network)
    with pytest.raises(EphemerisNotFoundError) as exc:
        load_ephemeris(tmp_path / "nope.bsp")
    assert "fetch_ephemeris" in str(exc.value)
    assert not (tmp_path / "nope.bsp").exists()


def test_kernel_is_loaded_once():
    if not default_kernel_path().exists():
        pytest.fail(f"Ephemeris kernel missing: {KERNEL_HELP}")
    assert get_ephemeris() is get_ephemeris()


def test_loading_opens_no_network_connection(monkeypatch):
    if not default_kernel_path().exists():
        pytest.fail(f"Ephemeris kernel missing: {KERNEL_HELP}")

    def no_network(*args, **kwargs):
        raise AssertionError("network access attempted")

    monkeypatch.setattr(socket.socket, "connect", no_network)
    load_ephemeris(default_kernel_path())
