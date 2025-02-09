import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, flash, url_for


def loadClubs():
    with open('clubs.json') as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showSummary', methods=['POST'])
def showSummary():
    now = str(datetime.now())
    clubsList = [club for club in clubs if club['email'] == request.form['email']]

    if len(clubsList) > 0:
        club = clubsList[0]
        return render_template('welcome.html', club=club, competitions=competitions, now=now)
    else:
        flash('Invalid email')
        return redirect(url_for('index'))


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    if placesRequired <= 12\
       and placesRequired <= int(competition['numberOfPlaces'])\
       and placesRequired <= int(club['points']):
        competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
        club['points'] = int(club['points']) - placesRequired
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=competitions)
    else:
        flash('Invalid booking')
        return redirect(url_for('book', competition=competition['name'], club=club['name']))


@app.route('/board')
def showPointsBoard():
    sortedClubs = sorted(clubs, key=lambda x: int(x['points']))
    return render_template('board.html', clubs=sortedClubs)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
