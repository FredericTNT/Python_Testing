import pytest
from models.models import Competition


@pytest.mark.parametrize("places, expected_value", [(5, '25'), (35, '-5'), (-7, '37')])
def test_competition_minusPlaces(places, expected_value):
    sut = Competition("$Première compétition!*", "2020-03-27 10:00:00", "30")
    sut.minusPlaces(places)
    assert sut.numberOfPlaces == expected_value
