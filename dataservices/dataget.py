def get_club_by_name(clubs, name):
    liste_club = [club for club in clubs if club.name == name]
    if liste_club:
        return liste_club[0]
    else:
        return None


def get_club_by_email(clubs, email):
    liste_club = [club for club in clubs if club.email == email]
    if liste_club:
        return liste_club[0]
    else:
        return None


def get_competition(competitions, name):
    liste_competition = [competition for competition in competitions if competition.name == name]
    if liste_competition:
        return liste_competition[0]
    else:
        return None
