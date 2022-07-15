from sqlalchemy import Column,Integer,String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
import json
from datetime import datetime

Base = declarative_base()

class Tournaments (Base):
    __tablename__ = 'Tournaments'
    id = Column(Integer, primary_key=True)
    location = Column(String(32))
    startdate = Column(Date)
    enddate = Column(Date)
    
    
class Matches(Base):
    __tablename__  = 'matches'
    id = Column(Integer, primary_key=True)
    tournament = Column(Integer)
    match_ranking = Column(String(2))
    date = Column(Date)
    player1 = Column(Integer)
    player2 = Column(Integer)
    winner = Column(Integer)
    losser = Column(Integer)
    
    def getJson(self):
        match_json = '{"id":"'+str(self.id)+'", "date":"'+str(self.date)+'", "player1":"'+str(self.player1)+'", "player2":"'+str(self.player2)+'", "winner":"'+str(self.winner)+'"}'
        print(match_json)
        return json.loads(match_json)
    
    
class Players(Base):
    __tablename__ = 'players'
    id = Column(Integer, primary_key=True)
    firstname = Column(String(32))
    lastname = Column(String(32))
    
    def getJson(self):
        player_json = '{"id":"'+str(self.id)+'", "firstname":"'+str(self.firstname)+'", "lastname":"'+str(self.lastname)+'"}'
        return json.loads(player_json)
    
match_ranking = ['F', 'S1', 'S2', 'Q1', 'Q2', 'Q3', 'Q4', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7','E8']

engine = create_engine('sqlite:///pilkarzyki.db', echo=True, connect_args={"check_same_thread": False})


Base.metadata.create_all(engine)


