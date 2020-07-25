# 1. import everything
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import pandas as pd

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement

Station = Base.classes.station
 
#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################


@app.route("/")
def home():
    """List of all available api routes"""
    return (
        f"Available Routes: <br/> "
        f"/api/v1.0/precipitation <br/> "
        f"/api/v1.0/stations <br/> "
        f"/api/v1.0/tobs <br/> "
        f"/api/v1.0/start <br/>"
        f"/api/v1.0/start/end"
        )


# 4. Define what to do when a user hits the /precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query date, precipitation
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Convert list of tuples into normal list
    all_dates = []
    for date, prcp in results:
        dates_dict = {}
        dates_dict["date"] = date
        dates_dict["prcp"] = prcp
        all_dates.append(dates_dict)

    return jsonify(all_dates)

@app.route("/api/v1.0/stations")
def station():
    session = Session(engine)

    results = session.query(Station.station).all()
    session.close()

    all_station = []
    for station in results:
        station_dict = {}
        station_dict["station"] = station
        all_station.append(station_dict)
    
    return jsonify(all_station)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.tobs, Measurement.station).filter(Measurement.date >= '2016-08-23').filter(Measurement.station == 'USC00519281').all()
    session.close()

    all_tobs = []
    for date, tob, station in results:
        tobs_dict = {}
        tobs_dict["tobs"] = tob
        tobs_dict["date"] = date
        tobs_dict["station"] = station
        all_tobs.append(tobs_dict)
    
    return jsonify(all_tobs)

@app.route("/api/v1.0/<start_d>")
def start(start_d):
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= start_d).all()
    session.close()

    all_start = []
    for date, tob in results:
        start_dict = {}
        start_dict["tobs"] = tob
        start_dict["date"] = date
        all_start.append(start_dict) 
    
    start_df = pd.DataFrame(all_start, columns = ['tobs', 'date'])
    start_df = start_df.set_index("date")
    min = start_df['tobs'].min()
    max = start_df['tobs'].max()
    mean = start_df['tobs'].mean()
    return (
        f"Mean: {mean}<br/> "
        f"Minimum: {min} <br/> "
        f"Maximum: {max}"
        )

@app.route("/api/v1.0/<start_d>/<end>")
def end(start_d, end):
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= start_d).filter(Measurement.date <= end).all()
    session.close()

    all_end = []
    for date, tob in results:
        end_dict = {}
        end_dict["tobs"] = tob
        end_dict["date"] = date
        all_end.append(end_dict) 
    
    end_df = pd.DataFrame(all_end, columns = ['tobs', 'date'])
    end_df = end_df.set_index("date")
    min = end_df['tobs'].min()
    max = end_df['tobs'].max()
    mean = end_df['tobs'].mean()
    return (
        f"Mean: {mean}<br/> "
        f"Minimum: {min} <br/> "
        f"Maximum: {max}"
        )
if __name__ == "__main__":
    app.run(debug=True)
