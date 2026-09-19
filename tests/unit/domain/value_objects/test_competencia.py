from datetime import date

import pytest

from app.domain.errors import ValidationError
from app.domain.value_objects.competencia import MAX_YEAR, MIN_YEAR, Competencia


@pytest.mark.parametrize(("entry", "esperado"), [("2026-08", (2026, 8)), ("08/2026", (2026, 8))])
def test_accepts_both_formats(entry, esperado):
    competencia = Competencia.parse(entry)
    assert (competencia.year, competencia.month) == esperado


def test_ignores_surrounding_spaces():
    assert Competencia.parse("  2026-08  ") == Competencia(2026, 8)


@pytest.mark.parametrize("entry", ["2026-13", "00/2026", "2026/08", "agosto", "", "2026-8"])
def test_rejection_invalid_format_or_month(entry):
    with pytest.raises(ValidationError):
        Competencia.parse(entry)


def test_wrong_type_rejection():
    with pytest.raises(ValidationError, match="deve ser texto"):
        Competencia.parse(202608)  # type: ignore[arg-type]


@pytest.mark.parametrize("month", [0, 13, -1])
def test_rejection_month_out_of_range(month):
    with pytest.raises(ValidationError, match="mês inválido"):
        Competencia(2026, month)


@pytest.mark.parametrize("year", [MIN_YEAR - 1, MAX_YEAR + 1])
def test_rejection_year_out_of_range(year):
    with pytest.raises(ValidationError, match="year out of range"):
        Competencia(year, 1)


def test_new_years_eve():
    assert Competencia(2026, 12).next() == Competencia(2027, 1)
    assert Competencia(2026, 1).previous() == Competencia(2025, 12)


def test_advances_and_reverts_within_the_year():
    assert Competencia(2026, 8).next() == Competencia(2026, 9)
    assert Competencia(2026, 8).previous() == Competencia(2026, 7)


def test_sorting_respects_year_before_month():
    assert Competencia(2025, 12) < Competencia(2026, 1)
    assert sorted([Competencia(2026, 3), Competencia(2025, 9)])[0] == Competencia(2025, 9)


def test_starting_from_date():
    assert Competencia.from_date(date(2026, 8, 27)) == Competencia(2026, 8)


def test_first_day():
    assert Competencia(2026, 8).first_day == date(2026, 8, 1)


def test_representations():
    competencia = Competencia(2026, 8)
    assert str(competencia) == "08/2026"
    assert competencia.iso == "2026-08"
    assert repr(competencia) == "Competencia('2026-08')"


def test_round_trip_iso():
    competencia = Competencia(2026, 8)
    assert Competencia.parse(competencia.iso) == competencia
    assert Competencia.parse(str(competencia)) == competencia


@pytest.mark.parametrize(("year", "month"), [("2026", 8), (2026, "08"), (2026.0, 8)])
def test_rejects_year_or_month_that_are_not_integers(year, month):
    with pytest.raises(ValidationError, match="inteiros"):
        Competencia(year, month)