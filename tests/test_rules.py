"""
Basic rule validation tests.
"""

from src.rules import is_excluded


def test_pepper_exclusion():
    assert is_excluded("black pepper chicken") is True


def test_safe_meal():
    assert is_excluded("grilled chicken with rice") is False


def test_pesto_exclusion():
    assert is_excluded("pesto pasta") is True
