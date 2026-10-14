"""Tests for the agent's tools."""

from datetime import date

import pytest

from agent import TAROT_CARDS, draw_tarot_card, get_today, get_zodiac_sign


@pytest.mark.parametrize(
    "birth_date, expected_sign",
    [
        ("1990-01-05", "Capricorn"),
        ("1990-01-20", "Aquarius"),
        ("1990-03-25", "Aries"),
        ("1990-07-15", "Cancer"),
        ("1990-12-21", "Sagittarius"),
        ("1990-12-30", "Capricorn"),
    ],
)
def test_get_zodiac_sign(birth_date, expected_sign):
    assert get_zodiac_sign.invoke({"birth_date": birth_date}) == expected_sign


def test_get_zodiac_sign_rejects_invalid_date():
    with pytest.raises(ValueError):
        get_zodiac_sign.invoke({"birth_date": "not-a-date"})


def test_draw_tarot_card_returns_known_card():
    card, orientation = draw_tarot_card.invoke({}).rsplit(" (", 1)
    assert card in TAROT_CARDS
    assert orientation in {"upright)", "reversed)"}


def test_get_today():
    assert get_today.invoke({}) == date.today().isoformat()