import pytest
from models.models import Competition, Club


@pytest.mark.parametrize("places, expected_value", [(5, '25'), (35, '-5'), (-7, '37')])
def test_competition_minusPlaces(places, expected_value):
    sut = Competition("$Première compétition!*", "2020-03-27 10:00:00", "30")
    sut.minusPlaces(places)
    assert sut.numberOfPlaces == expected_value


@pytest.mark.parametrize("points, expected_value", [(5, '10'), (35, '-20'), (-7, '22')])
def test_club_minusPoints(points, expected_value):
    sut = Club("$Premier club!*", "$club1@python.com.!*", "15")
    sut.minusPoints(points)
    assert sut.points == expected_value
