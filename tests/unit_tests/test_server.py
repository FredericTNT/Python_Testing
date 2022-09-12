import pytest
from models.models import Competition, Club
from server import create_app


@pytest.fixture
def client(mocker):
    """
    Initialisation de l'application Flask en mode test avec un jeu de données spécifiques
    """
    competitions = [Competition("$Première compétition!*", "2020-03-27 10:00:00", "30"),
                    Competition("$Seconde compétition!*", "2022-11-11 10:00:00", "20"),
                    Competition("$Troisième compétition!*", "2040-01-01 10:00:00", "10")]
    clubs = [Club("$Premier club!*", "$club1@python.com.!*", "15"),
             Club("$Second club!*", "$club2@python.com.!*", "10"),
             Club("$Troisième club!*", "$club3@python.com.!*", "5")]
    mocker.patch('dataservices.dataload.loadCompetitions', return_value=competitions)
    mocker.patch('dataservices.dataload.loadClubs', return_value=clubs)

    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client


def test_index(client):
    response = client.get('/')
    data = response.data.decode()
    assert response.status_code == 200
    assert data.find("<title>GUDLFT Registration</title>") != -1


def test_showSummary_ok(client, mocker):
    club = Club("$Premier club!*", "$club1@python.com.!*", "15")
    mocker.patch('dataservices.dataget.get_club_by_email', return_value=club)
    response = client.post('/showSummary', data={'email': club.email})
    data = response.data.decode()
    assert response.status_code == 200
    assert data.find("<title>Summary | GUDLFT Registration</title>") != -1


def test_showSummary_ko(client, mocker):
    email = "$Wrong@email!*"
    club = None
    mocker.patch('dataservices.dataget.get_club_by_email', return_value=club)
    response = client.post('/showSummary', data={'email': email})
    data = response.data.decode()
    assert response.status_code == 200
    assert data.find("<title>GUDLFT Registration</title>") != -1


def test_booking_ok(client, mocker):
    competition = Competition("$Seconde compétition!*", "2022-11-11 10:00:00", "20")
    club = Club("$Premier club!*", "$club1@python.com.!*", "15")
    mocker.patch('dataservices.dataget.get_club_by_name', return_value=club)
    mocker.patch('dataservices.dataget.get_competition', return_value=competition)
    response = client.get('/book/' + competition.name + '/' + club.name)
    data = response.data.decode()
    assert response.status_code == 200
    assert data.find("<title>Booking for " + competition.name + " || GUDLFT</title>") != -1


def test_booking_ko(client, mocker):
    mocker.patch('dataservices.dataget.get_club_by_name', return_value=None)
    mocker.patch('dataservices.dataget.get_competition', return_value=None)
    response = client.get('/book/$Wrong_competition*!/$Wrong_club*!')
    data = response.data.decode()
    assert response.status_code == 200
    assert data.find("<title>Summary | GUDLFT Registration</title>") != -1


def test_booking_past_competition(client, mocker):
    competition = Competition("$Première compétition!*", "2020-03-27 10:00:00", "30")
    club = Club("$Premier club!*", "$club1@python.com.!*", "15")
    mocker.patch('dataservices.dataget.get_club_by_name', return_value=club)
    mocker.patch('dataservices.dataget.get_competition', return_value=competition)
    response = client.get('/book/' + competition.name + '/' + club.name)
    data = response.data.decode()
    assert response.status_code == 200
    assert data.find("<title>Summary | GUDLFT Registration</title>") != -1


def test_purchase_ok(client, mocker):
    competition = Competition("$Seconde compétition!*", "2022-11-11 10:00:00", "20")
    club = Club("$Premier club!*", "$club1@python.com.!*", "15")
    places = 3
    mocker.patch('dataservices.dataget.get_competition', return_value=competition)
    mocker.patch('dataservices.dataget.get_club_by_name', return_value=club)
    response = client.post('/purchasePlaces', data={
        'competition': 'competition_name', 'club': 'club_name', 'places': places})
    data = response.data.decode()
    assert response.status_code == 200
    assert data.find("<title>Summary | GUDLFT Registration</title>") != -1
    assert data.find("Great-booking complete!") != -1
    assert competition.numberOfPlaces == '17'
    assert club.points == '12'


def test_purchase_not_enough_points(client, mocker):
    competition = Competition("$Seconde compétition!*", "2022-11-11 10:00:00", "20")
    club = Club("$Premier club!*", "$club1@python.com.!*", "5")
    places = 6
    mocker.patch('dataservices.dataget.get_competition', return_value=competition)
    mocker.patch('dataservices.dataget.get_club_by_name', return_value=club)
    response = client.post('/purchasePlaces', data={
        'competition': 'competition_name', 'club': 'club_name', 'places': places})
    data = response.data.decode()
    assert response.status_code == 200
    assert data.find("<title>Summary | GUDLFT Registration</title>") != -1
    assert data.find("Not enough points to book so many places") != -1
    assert competition.numberOfPlaces == '20'
    assert club.points == '5'


def test_purchase_more_than_12_places(client, mocker):
    competition = Competition("$Seconde compétition!*", "2022-11-11 10:00:00", "20")
    club = Club("$Premier club!*", "$club1@python.com.!*", "15")
    places = 13
    mocker.patch('dataservices.dataget.get_competition', return_value=competition)
    mocker.patch('dataservices.dataget.get_club_by_name', return_value=club)
    response = client.post('/purchasePlaces', data={
        'competition': 'competition_name', 'club': 'club_name', 'places': places})
    data = response.data.decode()
    assert response.status_code == 200
    assert data.find("<title>Summary | GUDLFT Registration</title>") != -1
    assert data.find("Booking more than 12 places per competition is not allowed") != -1
    assert competition.numberOfPlaces == '20'
    assert club.points == '15'


def test_purchase_bad_input(client, mocker):
    competition = Competition("$Seconde compétition!*", "2022-11-11 10:00:00", "20")
    club = Club("$Premier club!*", "$club1@python.com.!*", "15")
    places = '-3.0'
    mocker.patch('dataservices.dataget.get_competition', return_value=competition)
    mocker.patch('dataservices.dataget.get_club_by_name', return_value=club)
    response = client.post('/purchasePlaces', data={
        'competition': 'competition_name', 'club': 'club_name', 'places': places})
    data = response.data.decode()
    assert response.status_code == 200
    assert data.find("<title>Booking for " + competition.name + " || GUDLFT</title>") != -1
    assert data.find("You need to book a positive integer of places") != -1
    assert competition.numberOfPlaces == '20'
    assert club.points == '15'


def test_purchase_more_than_places_available(client, mocker):
    competition = Competition("$Seconde compétition!*", "2022-11-11 10:00:00", "3")
    club = Club("$Premier club!*", "$club1@python.com.!*", "15")
    places = 4
    mocker.patch('dataservices.dataget.get_competition', return_value=competition)
    mocker.patch('dataservices.dataget.get_club_by_name', return_value=club)
    response = client.post('/purchasePlaces', data={
        'competition': 'competition_name', 'club': 'club_name', 'places': places})
    data = response.data.decode()
    assert response.status_code == 200
    assert data.find("<title>Summary | GUDLFT Registration</title>") != -1
    assert data.find("You cannot book more than the number of places available") != -1
    assert competition.numberOfPlaces == '3'
    assert club.points == '15'


def test_logout_redirection_ok(client):
    response = client.get('/logout')
    assert response.status_code == 302
