from Models import Base, Tournaments, Matches, Players, match_ranking
from flask import Flask, jsonify, request, url_for, abort, g
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
import json
import random


#poolclass=SingletonThreadPool

engine = create_engine('sqlite:///pilkarzyki.db', echo=True, connect_args={"check_same_thread": False})

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)


@app.route('/addtournament', methods = ['POST'])
def new_tournament():
    location = request.json.get('location')
    startdate = request.json.get('startdate')
    enddate = request.json.get('enddate')
    if location is None or startdate is None or enddate is None:
        print("missing arguments")
        abort(400) 
        
    tournament = Tournaments()
    tournament.location = location
    tournament.startdate = datetime.strptime(startdate, '%d.%m.%Y').date()
    tournament.enddate = datetime.strptime(enddate, '%d.%m.%Y').date()
    
    session.add(tournament)
    session.commit()
    
    for ranking in match_ranking:
        match = Matches()
        match.tournament = tournament.id
        match.match_ranking = ranking
        session.add(match)
    
    session.commit()
    
    return jsonify({ 'Tournament': tournament.id }), 201
    




@app.route('/addplayer', methods = ['POST'])
def new_player():
    firstname = request.json.get('firstname')
    lastname = request.json.get('lastname')
    if firstname is None or lastname is None:
        print("missing arguments")
        abort(400) 
        
    if session.query(Players).filter_by(lastname = lastname).first() is not None:
        print("the player you are adding exists already!")
        player = session.query(Players).filter_by(lastname=lastname).first()
        return jsonify({'message':'player already exists'}), 200
        
    player = Players()
    player.lastname = lastname 
    player.firstname = firstname
    
    session.add(player)
    session.commit()
    return jsonify(player.getJson()), 201
    
    
@app.route('/initquartals/<int:id>')
def initiate_quartals(id):
    player_ids = list()
    quartal_finals = list()
    
    players = session.query(Players).all()
    matches = session.query(Matches).filter_by(tournament=id).all()

    
    for player in players:
        player_ids.append(player.id)
        
    for match in matches:
        if match.match_ranking.find("Q") == 0:
            quartal_finals.append(match)
            
    
    shuffled_player_ids = random.sample(player_ids, len(player_ids))
     
    for i in [0,1,2,3]:
        i1 = i*2
        i2 = i1+1
        quartal_finals[i].player1 = shuffled_player_ids[i1]
        quartal_finals[i].player2 = shuffled_player_ids[i2]
        session.add(quartal_finals[i])
        session.commit()
         
    
    return jsonify({'tounament': str(shuffled_player_ids)})
    

@app.route('/players/<int:id>')
def get_player(id):
    player = session.query(Players).filter_by(id=id).one()
    if not player:
        abort(400)
    return jsonify(player.getJson())

@app.route('/matches/<int:id>')
def get_matches(id):
    
    print("id: ", id)
    matches = session.query(Matches).filter_by(tournament=id).all()
    if not matches:
        abort(400)
    
   # print("First match is: ", matches[0])
    
    jsonStr = json.dumps(matches[0].__dict__)

    return jsonify({'Tournament': matches[0].tournament})


if __name__ == '__main__':
    app.debug = True
    app.run(host='localhost', port=5000)