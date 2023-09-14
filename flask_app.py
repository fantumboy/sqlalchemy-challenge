# 1. import Flask
from flask import Flask, jsonify

# 1a. other dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import func
import datetime as dt
import numpy as np

# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

engine = create_engine("sqlite:///Resources/hawaii.sqlite", echo=False)

Base = automap_base()
Base.prepare(autoload_with=engine)

Base.classes.keys()

M = Base.classes.measurement
S = Base.classes.station

    # # from instructor eli to confirm code was working
    # print([x.station for x in joined])

# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    print("server received request for home page")
    return(
            f"AVAILABLE ROUTES:<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/temp/startdate<br/>"
            f"/api/v1.0/temp/start/end<br/>"
        )

@app.route("/api/v1.0/precipitation")
def precipitation():
    print("server received request for precipitation page...")

    precip_dict = {}

    one_year = dt.date(2017, 8, 23) - dt.timedelta(days = 365)
    
    session = Session(engine)

    precip_12_months = session.query(M.date, M.prcp).filter(M.date >= one_year).all()

    session.close()

    for row in precip_12_months:
        date = row.date
        precipitation = row.prcp
        precip_dict[date] = precipitation

    precip_dict = list(np.ravel(precip_dict))

    return jsonify(precip_dict)


@app.route("/api/v1.0/stations")
def stations():
    print("server received request for stations page...")

    session = Session(engine)

    station_names = session.query(S.station).all()

    session.close()

    list_of_names = list(np.ravel(station_names))

    return jsonify(list_of_names)


@app.route("/api/v1.0/tobs")
def tobs():

    one_year = dt.date(2017, 8, 23) - dt.timedelta(days = 365)

    session = Session(engine)
    
    tobs_one_year = session.query(M.station, M.date, M.tobs).filter(M.station == 'USC00519281').filter(M.date >= one_year).all()

    session.close()

    tobs_dict = {}

    for row in tobs_one_year:
        date = row.date
        tobs = row.tobs
        tobs_dict[date] = tobs

    tobs_one_year = list(np.ravel(tobs_dict))

    return jsonify(tobs_one_year)


# <sd> and startdate(sd) idea in route from learning assistant sunshine
# sort of mimics the justice league classroom example below...
@app.route("/api/v1.0/temp/<sd>")
def sd_path(sd):

    start_date = dt.datetime.strptime(sd, '%m%d%Y').date()

    session = Session(engine)

    sel = [func.min(M.tobs), func.avg(M.tobs), func.max(M.tobs)]
    temps_sd = session.query(*sel).filter(M.date >= start_date).all()

    session.close()

    return jsonify(list(np.ravel(temps_sd)))


@app.route("/api/v1.0/temp/<sd>/<ed>")
def date_range(sd, ed):

    start_date = dt.datetime.strptime(sd, "%m%d%Y")
    end_date = dt.datetime.strptime(ed, "%m%d%Y")

    session = Session(engine)
    print(sd, ed)
    sel = [func.min(M.tobs), func.avg(M.tobs), func.max(M.tobs)]
    temps_sd_ed = session.query(*sel).filter(M.date >= start_date).filter(M.date <= end_date).all()

    session.close()

    return jsonify(list(np.ravel(temps_sd_ed)))

# 5. define main behavior

if __name__ == "__main__":
    app.run(debug=True)

