"""Tests for Home Chef menu URL generation."""

from datetime import date

import pytest

from tools.homechef_urls import (
    format_date,
    generate_dates,
    generate_url,
    generate_urls,
    get_starting_monday,
    next_monday,
    parse_date,
)


def test_monday_stays_monday():
    """A Monday should remain the starting Monday."""
    result = next_monday(date(2026, 8, 31))

    assert result == date(2026, 8, 31)


def test_wednesday_moves_to_following_monday():
    """A Wednesday should move forward to the following Monday."""
    result = next_monday(date(2026, 8, 26))

    assert result == date(2026, 8, 31)


def test_sunday_moves_to_next_day_monday():
    """A Sunday should move forward one day to Monday."""
    result = next_monday(date(2026, 8, 30))

    assert result == date(2026, 8, 31)


def test_tuesday_moves_to_following_monday():
    """A Tuesday should move forward to the following Monday."""
    result = next_monday(date(2026, 9, 1))

    assert result == date(2026, 9, 7)


def test_starting_monday_with_given_monday():
    """A supplied Monday should be used unchanged."""
    result = get_starting_monday(date(2026, 8, 31))

    assert result == date(2026, 8, 31)


def test_starting_monday_with_given_non_monday():
    """A supplied non-Monday should advance to the next Monday."""
    result = get_starting_monday(date(2026, 8, 26))

    assert result == date(2026, 8, 31)


def test_starting_monday_without_date(monkeypatch):
    """No supplied date should use today's date and find the next Monday."""
    class FakeDate(date):
        @classmethod
        def today(cls):
            return cls(2026, 8, 26)

    monkeypatch.setattr("tools.homechef_urls.date", FakeDate)

    result = get_starting_monday()

    assert result == date(2026, 8, 31)


def test_generate_one_week():
    """One requested week should produce exactly one Monday."""
    result = generate_dates(date(2026, 8, 31), 1)

    assert result == [date(2026, 8, 31)]


def test_generate_five_weeks():
    """Five requested weeks should produce five consecutive Mondays."""
    result = generate_dates(date(2026, 8, 31), 5)

    assert result == [
        date(2026, 8, 31),
        date(2026, 9, 7),
        date(2026, 9, 14),
        date(2026, 9, 21),
        date(2026, 9, 28),
    ]


def test_generated_dates_are_seven_days_apart():
    """Each generated menu date should be exactly seven days apart."""
    result = generate_dates(date(2026, 8, 31), 5)

    for first, second in zip(result, result[1:]):
        assert (second - first).days == 7


def test_zero_weeks_is_rejected():
    """Zero weeks should not generate any URLs."""
    with pytest.raises(ValueError, match="at least 1"):
        generate_dates(date(2026, 8, 31), 0)


def test_negative_weeks_is_rejected():
    """Negative weeks should not be accepted."""
    with pytest.raises(ValueError, match="at least 1"):
        generate_dates(date(2026, 8, 31), -1)


def test_parse_valid_date():
    """Home Chef's lowercase date format should parse correctly."""
    result = parse_date("31-aug-2026")

    assert result == date(2026, 8, 31)


def test_parse_date_is_case_insensitive():
    """Month capitalization should not affect parsing."""
    result = parse_date("31-AUG-2026")

    assert result == date(2026, 8, 31)


def test_invalid_date_is_rejected():
    """Impossible calendar dates should be rejected."""
    with pytest.raises(ValueError, match="Invalid date"):
        parse_date("31-feb-2026")


def test_invalid_date_format_is_rejected():
    """Dates using the wrong format should be rejected."""
    with pytest.raises(ValueError, match="Invalid date"):
        parse_date("2026-08-31")


def test_invalid_text_is_rejected():
    """Non-date input should be rejected."""
    with pytest.raises(ValueError, match="Invalid date"):
        parse_date("banana")


def test_format_date_matches_home_chef_format():
    """Dates should use lowercase DD-mon-YYYY formatting."""
    result = format_date(date(2026, 8, 31))

    assert result == "31-aug-2026"


def test_generate_url():
    """The correct Home Chef API URL should be generated."""
    result = generate_url(date(2026, 8, 31))

    assert (
        result
        == "https://www.homechef.com/api/v3/menus/"
        "31-aug-2026/standard/meals"
    )


def test_generate_urls_finds_next_monday():
    """A Wednesday should produce the following Monday's URL."""
    result = generate_urls(date(2026, 8, 26), 1)

    assert result == [
        (
            date(2026, 8, 31),
            "https://www.homechef.com/api/v3/menus/"
            "31-aug-2026/standard/meals",
        )
    ]


def test_generate_urls_for_multiple_weeks():
    """Multiple requested weeks should produce consecutive menu URLs."""
    result = generate_urls(date(2026, 8, 26), 3)

    assert [menu_date for menu_date, _ in result] == [
        date(2026, 8, 31),
        date(2026, 9, 7),
        date(2026, 9, 14),
    ]

    assert [url for _, url in result] == [
        "https://www.homechef.com/api/v3/menus/"
        "31-aug-2026/standard/meals",
        "https://www.homechef.com/api/v3/menus/"
        "07-sep-2026/standard/meals",
        "https://www.homechef.com/api/v3/menus/"
        "14-sep-2026/standard/meals",
    ]