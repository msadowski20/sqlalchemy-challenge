import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import datetime as dt

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
measurement = Base.classes.passenger
station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

app = Flask(__name__)

@app.route("/")
def home():
    return(
        f"Welcome to the Climate Analysis API!"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query measurement table for date and precipitation
    results = session.query(measurement.date, measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of dates and precipitation
    precip_list = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["precipitation"] = prcp
        precip_list.append(precip_dict)

    return jsonify(precip_list)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query station table for station name
    results = session.query(station.name).all()

    session.close()

    # Convert list of tuples into normal list
    station_names = list(np.ravel(results))

    return jsonify(station_names)


@app.route("/api/v1.0/tobs")
def tobs():

    last_day = dt.date(2017, 8, 23)
    year_ago = last_day - dt.timedelta(days=365)
    most_active = "USC00519397"

    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query station table for station name
    results = session.query(measurement.tobs).\
        filter(measurement.station == most_active)
        filter(measurement.date >= year_ago).\
        filter(measurement.date <= last_day).\
        order_by(measurement.date).all()

    session.close()

    # Convert list of tuples into normal list
    station_temps = list(np.ravel(results))

    return jsonify(station_temps)


@app.route("/api/v1.0/<start>")
def start():






if __name__ == '__main__':
    app.run(debug=True)




