   # Import the dependencies.

import numpy as np
import pandas as pd
import datetime as dt

from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################

engine = create_engine('sqlite:///Resources/hawaii.sqlite', connect_args={'check_same_thread': False})
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)


#################################################
# Flask Routes

@app.route("/")
def welcome():
    return (
        f"<p>Welcome </p>"
        f"<p>Usage:</p>"
        f"/api/v1.0/precipitation<br/>Returns a JSON list of percipitation data for the specific dates <br/><br/>"
        f"/api/v1.0/stations<br/>Returns a JSON list of the weather stations<br/><br/>"
        f"/api/v1.0/tobs<br/>Returns a JSON list of the Temperature Observations (tobs) for each station for specific dates<br/><br/>"
        f"/api/v1.0/date<br/>Returns a JSON list of the minimum, average, max temperature for the dates<br/><br/>."
        f"/api/v1.0/start_date/end_date<br/>Returns a JSON list of the minimum temperature, the average temperature, and the max temperature for the dates between the given start date and end date<br/><br/>.")
#################################################
#Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
#Return the JSON representation of your dictionary.

@app.route("/api/v1.0/precipitation")
def prcp():
    session = Session(engine)
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= query_date).all()
    all_prcp = list(np.ravel(results))
    session.close()
    return jsonify(all_prcp)
    
  #Return a JSON list of stations from the dataset.  
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    results = session.query(Station.station, Station.name).all()
    session.close()
    all_stations =[]
    for station in results:
        station_dict ={}
        station_dict["station"] = station[0]
        station_dict["name"] = station[1]
        all_stations.append(station_dict)
    return jsonify(all_stations)

# Query the dates and temperature observations of the most-active station for the previous year of data.
# Return a JSON list of temperature observations for the previous year.
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    active_station = 'USC00519281'
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).filter_by(station=active_station).first()[0]
    query_date = dt.datetime.strptime(latest_date, '%Y-%m-%d') - dt.timedelta(days=365)
    temperature = session.query(Measurement.tobs).filter(Measurement.station == active_station).filter(Measurement.date >= query_date).all()
    session.close()
    temp_list = list(np.ravel(temperature))
    return jsonify(temp_list)

#start and end api               
                     
@app.route("/api/v1.0/<start>")
def start_date(start):
    # Create a session from Python to the DB
    session = Session(engine)

    # Define the start date and query the min, avg, and max temperature for all dates greater than or equal to the start date
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()

    # Close the session
    session.close()
    return jsonify(results)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start, end):
    # Create a session from Python to the DB
    session = Session(engine)
    # Define the start and end date and query the min, avg, and max temperature for all dates between the start and end date, inclusive
    start_date = dt.datetime.strptime(start, '%Y-%m-%d')
    end_date = dt.datetime.strptime(end, '%Y-%m-%d')
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    all_tobs = []
    for Tmin, Tavg, Tmax in results:
        tobs_dict = {}
        tobs_dict["TMIN"] = Tmin
        tobs_dict["TAVG"] = Tavg
        tobs_dict["TMAX"] = Tmax
        all_tobs.append(tobs_dict)    
    session.close()
    return jsonify(all_tobs)
                 
if __name__ == '__main__':
    app.run(debug=True)

                     
                     
                     
                     
                     
                     
                     
                     
                     
                     
                     
                     
                     
                     
                     
                     
                     
                     
                     
                     
                     
                     
                     
                     
                     
                     
                     
                     
                     
                     
                     
                     
                     