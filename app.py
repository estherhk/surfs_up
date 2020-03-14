#import dependencies
import datetime as dt
import numpy as np
import pandas as pd

#import SQLAlchemy
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#import dependencies for Flask
from flask import Flask, jsonify

#set up database engine
engine = create_engine("sqlite:///hawaii.sqlite")

#reflect database
Base = automap_base()
Base.prepare(engine, reflect=True)
#save references
Measurement = Base.classes.measurement
Station = Base.classes.station
#create session link
session = Session(engine)

#set up Flask
app = Flask(__name__)

#Create Welcome route (9.5.2)
@app.route("/")
def welcome():
    return(
        '''
        Welcome to the Climate Analysis API!
        Available Routes:
        /api/v1.0/precipitation
        /api/v1.0/stations
        /api/v1.0/tobs
        /api/v1.0/temp/start/end
        ''')

#Create Precitipation route (9.5.3)
@app.route("/api/v1.0/precipitation")
def precipitation():
   prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
   precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
   precip = {date: prcp for date, prcp in precipitation}
   return jsonify(precip)

#Create Station Route (9.5.4)   
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations)

#Create Monthly Temperature Route
@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))

    return jsonify(temps)

#Create Statistics Route (9.5.6)
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]           
         
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date <= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)
        
    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)

if __name__ == '__main__':
    app.run()  