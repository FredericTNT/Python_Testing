import pytest
from models.models import Competition, Club
from dataservices import dataget, dataload


@pytest.fixture
def data_environnement():
    competitions = [Competition("$Première compétition!*", "2020-03-27 10:00:00", "30"),
                    Competition("$Seconde compétition!*", "2022-11-11 10:00:00", "20"),
                    Competition("$Troisième compétition!*", "2040-01-01 10:00:00", "10")]
    clubs = [Club("$Premier club!*", "$club1@python.com.!*", "15"),
             Club("$Second club!*", "$club2@python.com.!*", "10"),
             Club("$Troisième club!*", "$club3@python.com.!*", "5")]
    data = {"competitions": competitions, "clubs": clubs}
    return data


class TestDataget:

    def test_get_club_by_name_ok(self, data_environnement):
        name = "$Second club!*"
        expected_value = "$club2@python.com.!*"
        assert dataget.get_club_by_name(data_environnement["clubs"], name).email == expected_value

    def test_get_club_by_name_ko(self, data_environnement):
        name = "$Wrong name!*"
        expected_value = None
        assert dataget.get_club_by_name(data_environnement["clubs"], name) == expected_value

    def test_get_club_by_email_ok(self, data_environnement):
        email = "$club2@python.com.!*"
        expected_value = "$Second club!*"
        assert dataget.get_club_by_email(data_environnement["clubs"], email).name == expected_value

    def test_get_club_by_email_ko(self, data_environnement):
        email = "$Wrong@email!*"
        expected_value = None
        assert dataget.get_club_by_email(data_environnement["clubs"], email) == expected_value

    def test_get_competition_by_name_ok(self, data_environnement):
        name = "$Première compétition!*"
        expected_value = "2020-03-27 10:00:00"
        assert dataget.get_competition(data_environnement["competitions"], name).date == expected_value

    def test_get_competition_by_name_ko(self, data_environnement):
        name = "$Wrong name!*"
        expected_value = None
        assert dataget.get_competition(data_environnement["competitions"], name) == expected_value


class TestDataload:

    def test_loadCompetitions(self):
        expected_value = "Spring Festival"
        assert dataload.loadCompetitions()[0].name == expected_value

    def test_loadClubs(self):
        expected_value = "admin@irontemple.com"
        assert dataload.loadClubs()[1].email == expected_value
