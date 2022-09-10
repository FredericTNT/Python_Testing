import json
from models.models import Club, Competition


def loadClubs():
    with open('clubs.json') as clubs:
        data = json.load(clubs)['clubs']
        list_of_clubs = []
        for item in data:
            list_of_clubs.append(Club(item['name'], item['email'], item['points']))
        return list_of_clubs


def loadCompetitions():
    with open('competitions.json') as competitions:
        data = json.load(competitions)['competitions']
        list_of_competitions = []
        for item in data:
            list_of_competitions.append(Competition(item['name'], item['date'], item['numberOfPlaces']))
        return list_of_competitions
