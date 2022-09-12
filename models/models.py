class Club:

    def __init__(self, name, email, points):
        self.name = name
        self.email = email
        self.points = points

    def __repr__(self):
        return self.name

    def minusPoints(self, points):
        self.points = str(int(self.points) - points)


class Competition:

    def __init__(self, name, date, number_of_places):
        self.name = name
        self.date = date
        self.numberOfPlaces = number_of_places

    def __repr__(self):
        return self.name

    def minusPlaces(self, places):
        self.numberOfPlaces = str(int(self.numberOfPlaces) - places)
