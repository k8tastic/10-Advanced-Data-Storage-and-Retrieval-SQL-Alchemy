import numpy as np
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

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

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# Define what to do when a user hits the index route
@app.route("/")
def routes():
    print("Server received request for 'Home' page...")
    return (
        f"Available Routes:<br/>"
        f"/about<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Station.station).all()
    list_stations = list(np.ravel(stations))
    return jsonify(list_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    annual_temp = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= last_date).\
        order_by(Measurement.date).all()
        
    temp_values = []
    for observation in annual_temp:
        temp_dict = {}
        temp_dict [observation.date] = observation.tobs
        temp_values.append(temp_dict )

    return jsonify(temp_values)


if __name__ == "__main__":
    app.run(debug=True)