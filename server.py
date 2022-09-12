from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime
from dataservices import dataload, dataget
from utilities import inputcontrol


def create_app(testing_mode):
    app = Flask(__name__)
    app.config.from_object("config")
    app.config["TESTING"] = testing_mode.get("TESTING")

    competitions = dataload.loadCompetitions()
    clubs = dataload.loadClubs()

    @app.route('/')
    def index():
        """
        Affichage de la page d'accueil du site
        """
        return render_template('index.html')

    @app.route('/showSummary', methods=['POST'])
    def showSummary():
        """
        Affichage du sommaire du site et de la liste des compétitions à réserver après vérification
        de l'identifiant du club (adresse email)

        """
        club = dataget.get_club_by_email(clubs, request.form['email'])
        if club:
            return render_template('welcome.html', club=club, competitions=competitions)
        else:
            flash("Wrong email, please try again")
            return render_template('index.html')

    @app.route('/book/<competition>/<club>')
    def book(competition, club):
        """
        Affichage de la page de réservation d'une compétition après vérification des identifiants du club (nom)
        et de la compétition (nom)
        """
        foundClub = dataget.get_club_by_name(clubs, club)
        foundCompetition = dataget.get_competition(competitions, competition)
        if foundClub and foundCompetition:
            if datetime.fromisoformat(foundCompetition.date) > datetime.today():
                return render_template('booking.html', club=foundClub, competition=foundCompetition)
            else:
                flash("You cannot book a past competition")
        else:
            flash("Something went wrong-please try again")
        return render_template('welcome.html', club=foundClub, competitions=competitions)

    @app.route('/purchasePlaces', methods=['POST'])
    def purchasePlaces():
        """
        Affichage du sommaire du site après mise à jour des éléments de la réservation
        """
        RATIO_POINTS_PLACES = 1
        competition = dataget.get_competition(competitions, request.form['competition'])
        club = dataget.get_club_by_name(clubs, request.form['club'])
        if not inputcontrol.is_positive_integer(request.form['places']):
            flash('You need to book a positive integer of places')
            return render_template('booking.html', club=club, competition=competition)
        placesRequired = int(request.form['places'])
        pointsNeeded = placesRequired * RATIO_POINTS_PLACES
        if pointsNeeded > int(club.points):
            flash("Not enough points to book so many places")
        elif placesRequired > 12:
            flash("Booking more than 12 places per competition is not allowed")
        else:
            competition.minusPlaces(placesRequired)
            club.minusPoints(pointsNeeded)
            flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=competitions)

    # TODO: Add route for points display

    @app.route('/logout')
    def logout():
        """
        Déconnexion et redirection vers la page d'accueil du site
        """
        return redirect(url_for('index'))

    return app


app = create_app({"TESTING": False})

if __name__ == '__main__':
    app.run()
