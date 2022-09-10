def get_club_by_name(clubs, name):
    return [club for club in clubs if club.name == name][0]


def get_club_by_email(clubs, email):
    return [club for club in clubs if club.email == email][0]


def get_competition(competitions, name):
    return [competition for competition in competitions if competition.name == name][0]
