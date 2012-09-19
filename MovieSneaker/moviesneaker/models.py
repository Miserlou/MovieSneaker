from flask.ext.sqlalchemy import SQLAlchemy

from moviesneaker import app

db = SQLAlchemy(app)

class Zipcode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    zipcode = db.Column(db.String(60), unique=True)
class Movie(db.Model):
    name = db.Column(db.String(256))
    runtime = models.IntegerField() # in minutes
    description = db.Column(db.String(512))
    notes = db.Column(db.String(1024))

class Venue(db.Model):
    name = db.Column(db.String(256)),
    address = db.Column(db.String(512)),
    # This isn't the actual zipcode this venue is in
    # Just the set of zipcodes this is considered close to
    zipcode = models.ManyToManyField(ZipCode)
    description = db.Column(db.String(1024))

class Showing(db.Model):
    movie = models.ForeignKey(Movie)
    venue = models.ForeignKey(Venue)
    start = models.DateTimeField()
    end = models.DateTimeField()
