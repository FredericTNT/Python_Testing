import os
import sys
import json
from models.models import Club, Competition


def loadClubs():
    file_name = 'clubs.json'
    if len(sys.argv) != 1 and os.path.exists(os.path.join(sys.argv[1], file_name)):
        file_name = os.path.join(sys.argv[1], file_name)
    with open(file_name) as clubs:
        data = json.load(clubs)['clubs']
        list_of_clubs = []
        for item in data:
            list_of_clubs.append(Club(item['name'], item['email'], item['points']))
        return list_of_clubs


def loadCompetitions():
    file_name = 'competitions.json'
    if len(sys.argv) != 1 and os.path.exists(os.path.join(sys.argv[1], file_name)):
        file_name = os.path.join(sys.argv[1], file_name)
    with open(file_name) as competitions:
        data = json.load(competitions)['competitions']
        list_of_competitions = []
        for item in data:
            list_of_competitions.append(Competition(item['name'], item['date'], item['numberOfPlaces']))
        return list_of_competitions
