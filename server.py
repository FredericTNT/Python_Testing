from flask import Flask, render_template, request, redirect, flash, url_for
from dataservices import dataload, dataget


def create_app(testing_mode):
    app = Flask(__name__)
    app.config.from_object("config")
    app.config["TESTING"] = testing_mode.get("TESTING")

    competitions = dataload.loadCompetitions()
    clubs = dataload.loadClubs()

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/showSummary', methods=['POST'])
    def showSummary():
        club = dataget.get_club_by_email(clubs, request.form['email'])
        return render_template('welcome.html', club=club, competitions=competitions)

    @app.route('/book/<competition>/<club>')
    def book(competition, club):
        foundClub = dataget.get_club_by_name(clubs, club)
        foundCompetition = dataget.get_competition(competitions, competition)
        if foundClub and foundCompetition:
            return render_template('booking.html', club=foundClub, competition=foundCompetition)
        else:
            flash("Something went wrong-please try again")
            return render_template('welcome.html', club=club, competitions=competitions)

    @app.route('/purchasePlaces', methods=['POST'])
    def purchasePlaces():
        competition = dataget.get_competition(competitions, request.form['competition'])
        club = dataget.get_club_by_name(clubs, request.form['club'])
        placesRequired = int(request.form['places'])
        competition.minusPlaces(placesRequired)
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=competitions)

    # TODO: Add route for points display

    @app.route('/logout')
    def logout():
        return redirect(url_for('index'))

    return app


app = create_app({"TESTING": False})

if __name__ == '__main__':
    app.run()
