import pytest
from models.models import Competition, Club
from server import create_app


@pytest.fixture
def client():
    """
    Initialisation de l'application Flask en mode test
    """
    app = create_app({"TESTING": True})
    with app.test_client() as client:
        yield client


def test_user_story_1(client):
    """
    Parcours client #1 (mode client Flask off-line)
        - Identification via adresse email
        - Choix de la compétition
        - Réservation des places
        > Confirmation de la réservation
    """
    competition_name = "Spring Festival"
    club_name = "Simply Lift"
    club_email = "john@simplylift.co"
    places = 3
    response = client.post('/showSummary', data={'email': club_email})
    assert response.status_code == 200
    response = client.get('/book/' + competition_name + '/' + club_name)
    assert response.status_code == 200
    response = client.post('/purchasePlaces', data={
        'competition': competition_name, 'club': club_name, 'places': places})
    data = response.data.decode()
    assert response.status_code == 200
    assert data.find("Great-booking complete!") != -1
