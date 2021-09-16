# REMEMBER, FLASK IS RAN FROM CDM LINE 
# import dependencies 
import datetime as dt
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify


# set up our database engine for the Flask application, 
# The "create_engine()"" function allows us to access and query our SQLite database file. 
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect the database into our classes
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# create a variable for each of the classes so that we can reference them later
Measurement = Base.classes.measurement
Station = Base.classes.station

# create a session link from Python to our database with the following code
session = Session(engine)

# create a session link from Python to the database
app = Flask(__name__)

##IMPORTANT
#All of your routes should go after the app = Flask(__name__) line of code. Otherwise, your code may not run properly.

# **Note: Every time you create a new route, your code should be aligned to the left in order to avoid errors.**
@app.route('/')

# create a function welcome() with a return statement
# add the routing information for each of the other routes
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
    # /api/v1.0/ followed by the name of the route. This convention signifies that this is version 1 of our application
    # This line can be updated to support future versions of the app as well.

# Create precipitation route
@app.route("/api/v1.0/precipitation")

#  create the precipitation() function
def precipitation():
    # First, we want to add the line of code that calculates the date one year ago from the most recent date in the database
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # write a query to get the date and precipitation for the previous year.
     # Note: You can use the combination of .\ to shorten the length of your query line so that it extends to the next line
    precipitation = session.query(Measurement.date, Measurement.prcp).\
      filter(Measurement.date >= prev_year).all()
    #create a dictionary{} with the date as the key and the precipitation as the value
    precip = {date: prcp for date, prcp in precipitation}
    #use jsonify() to format our results into a JSON structured file
    return jsonify(precip)

#  create the route and stations() function
@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# create route and  temp_monthy() function 
@app.route("/api/v1.0/tobs")
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # query the primary station for all the temperature observations from the previous year.
    # and unravel the results into a one-dimensional array and convert that array into a list
    results = session.query(Measurement.tobs).\
      filter(Measurement.station == 'USC00519281').\
      filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# Create a minimum, average, and maximum temperatures route(s) & function stats ()
# Note: in the following code, take note of the asterisk in the query next to the
# sel list. Here the asterisk is used to indicate there will be multiple results 
# for our query: minimum, average, and maximum temperatures.
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)