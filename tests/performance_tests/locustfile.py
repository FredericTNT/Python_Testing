from locust import HttpUser, task


class ProjectPerfTest(HttpUser):
    @task
    def index(self):
        self.client.get("/")

    @task
    def showSummary(self):
        email = 'admin@irontemple.com'
        self.client.post('/showSummary', data={'email': email})

    @task(2)
    def booking(self):
        competition = "Spring Festival"
        club = "Iron Temple"
        self.client.get('/book/' + competition + '/' + club)

    @task(2)
    def purchase(self):
        competition = "Spring Festival"
        club = "Iron Temple"
        self.client.post('/purchasePlaces', data={'competition': competition, 'club': club, 'places': 5})
