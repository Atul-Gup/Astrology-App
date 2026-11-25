import csv
from datetime import UTC, date, datetime, time, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

from calc.timeplace import (
    AmbiguousLocalTimeError,
    InvalidCoordinatesError,
    InvalidTimezoneError,
    NonexistentLocalTimeError,
    local_to_utc,
    validate_coordinates,
)

KOLKATA = "Asia/Kolkata"
NEW_YORK = "America/New_York"


def test_kolkata_2000_is_utc_plus_5_30():
    r = local_to_utc(date(2000, 6, 15), time(12, 0), KOLKATA)
    assert r.utc == datetime(2000, 6, 15, 6, 30, tzinfo=UTC)
    assert r.utc_offset == timedelta(hours=5, minutes=30)
    assert r.tz_name == KOLKATA


def test_local_is_returned_with_timezone_name_and_offset():
    r = local_to_utc(date(2000, 6, 15), time(12, 0), KOLKATA)
    assert r.local.replace(tzinfo=None) == datetime(2000, 6, 15, 12, 0)
    assert r.local.utcoffset() == timedelta(hours=5, minutes=30)


def test_result_utc_is_utc_aware():
    r = local_to_utc(date(1990, 1, 1), time(8, 30), KOLKATA)
    assert r.utc.tzinfo is UTC or r.utc.utcoffset() == timedelta(0)


def test_leap_day():
    r = local_to_utc(date(2000, 2, 29), time(10, 15), KOLKATA)
    assert r.utc == datetime(2000, 2, 29, 4, 45, tzinfo=UTC)


def test_midnight_birth_changes_utc_date():
    r = local_to_utc(date(2000, 3, 1), time(0, 0), KOLKATA)
    assert r.utc == datetime(2000, 2, 29, 18, 30, tzinfo=UTC)


def test_late_evening_birth_stays_same_utc_date():
    r = local_to_utc(date(2000, 3, 1), time(23, 59), KOLKATA)
    assert r.utc == datetime(2000, 3, 1, 18, 29, tzinfo=UTC)


@pytest.mark.parametrize("year", [1955, 1975, 1995, 2023])
def test_several_decades_round_trip(year):
    d, t = date(year, 7, 1), time(14, 30)
    r = local_to_utc(d, t, NEW_YORK)
    back = r.utc.astimezone(ZoneInfo(NEW_YORK))
    assert (back.date(), back.time()) == (d, t)


def test_daylight_saving_offset_differs_from_winter():
    summer = local_to_utc(date(2021, 7, 1), time(12, 0), NEW_YORK)
    winter = local_to_utc(date(2021, 1, 1), time(12, 0), NEW_YORK)
    assert summer.utc_offset == timedelta(hours=-4)
    assert winter.utc_offset == timedelta(hours=-5)


def test_nonexistent_local_time_in_clock_forward_gap_is_rejected():
    with pytest.raises(NonexistentLocalTimeError) as exc:
        local_to_utc(date(2021, 3, 14), time(2, 30), NEW_YORK)
    assert "2021-03-14" in str(exc.value)
    assert NEW_YORK in str(exc.value)


def test_ambiguous_local_time_in_clock_back_overlap_is_rejected():
    with pytest.raises(AmbiguousLocalTimeError) as exc:
        local_to_utc(date(2021, 11, 7), time(1, 30), NEW_YORK)
    assert "2021-11-07" in str(exc.value)
    assert NEW_YORK in str(exc.value)


def test_times_just_around_the_gap_succeed():
    before = local_to_utc(date(2021, 3, 14), time(1, 59), NEW_YORK)
    after = local_to_utc(date(2021, 3, 14), time(3, 0), NEW_YORK)
    assert before.utc_offset == timedelta(hours=-5)
    assert after.utc_offset == timedelta(hours=-4)


def test_times_just_around_the_overlap_succeed():
    before = local_to_utc(date(2021, 11, 7), time(0, 59), NEW_YORK)
    after = local_to_utc(date(2021, 11, 7), time(2, 0), NEW_YORK)
    assert before.utc_offset == timedelta(hours=-4)
    assert after.utc_offset == timedelta(hours=-5)


def test_invalid_timezone_name_is_rejected():
    with pytest.raises(InvalidTimezoneError):
        local_to_utc(date(2000, 1, 1), time(12, 0), "Not/AZone")


@pytest.mark.parametrize("name", ["", "../etc/passwd", "Asia/../Kolkata"])
def test_malformed_timezone_names_are_rejected(name):
    with pytest.raises(InvalidTimezoneError):
        local_to_utc(date(2000, 1, 1), time(12, 0), name)


def test_aware_time_is_rejected():
    with pytest.raises(ValueError, match="naive"):
        local_to_utc(date(2000, 1, 1), time(12, 0, tzinfo=UTC), KOLKATA)


@pytest.mark.parametrize("lat,lon", [(0, 0), (28.6, 77.2), (-90, 180), (90, -180), (-33.9, 151.2)])
def test_valid_coordinates_accepted(lat, lon):
    validate_coordinates(lat, lon)


@pytest.mark.parametrize(
    "lat,lon",
    [(90.1, 0), (-90.1, 0), (0, 180.1), (0, -180.1), (float("nan"), 0), (0, float("inf"))],
)
def test_invalid_coordinates_rejected(lat, lon):
    with pytest.raises(InvalidCoordinatesError):
        validate_coordinates(lat, lon)


# The golden CSV has no UTC or offset column, so this can only check that every golden case
# resolves cleanly (valid zone, not in a gap or overlap). It cannot verify the offset itself.
GOLDEN = Path(__file__).resolve().parents[3] / "data" / "golden" / "golden-charts.csv"


def test_golden_cases_resolve_without_error():
    if not GOLDEN.exists():
        pytest.skip("data/golden/golden-charts.csv not created yet (founder task H1)")
    with GOLDEN.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        pytest.skip("golden-charts.csv has no cases yet")
    for row in rows:
        d = date.fromisoformat(row["birth_date"])
        t = time.fromisoformat(row["birth_time_local"])
        local_to_utc(d, t, row["timezone_name"])
        validate_coordinates(float(row["latitude"]), float(row["longitude"]))
