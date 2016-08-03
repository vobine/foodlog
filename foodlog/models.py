import datetime as dt
import sqlalchemy as sql
import sqlalchemy.orm as orm
import sqlalchemy.ext.declarative as sqldcl
from passlib.hash import bcrypt_sha256 as bcrypt
import flask_login

# Preliminaries
Base = sqldcl.declarative_base ()

# Unit juggling
class WeightUnit:
    """Give names to (too many!) units of weight."""
    def __init__ (self, name, abbreviation, grams):
        """A unit has a long and short name, and a canonical value in grams."""
        self.name = name
        self.abbreviation = abbreviation
        self.grams = grams

    def fromGrams (self, grams):
        """Convert a value in grams to this unit."""
        return grams / self.grams

    def toGrams (self, value):
        """Convert a value in this unit to grams."""
        return value * self.grams

_weights = dict (kg = WeightUnit ('kilogram', 'kg', 1000.0),
                 g = WeightUnit ('gram', 'g', 1.0),
                 st = WeightUnit ('stone', 'st', 6350.29318),
                 lb = WeightUnit ('pound', 'lb', 453.59237))
_weightNames = frozenset (w.abbreviation for w in _weights.values ())

# Table/class declarations

class User (Base, flask_login.UserMixin):
    """A User is a User for Flask-login credentials."""
    __tablename__ = 'users'

    id = sql.Column (sql.Integer, primary_key=True)
    name = sql.Column (sql.String (CHAR_LIMITS['name']))
    hashPass = sql.Column (sql.String (150), nullable=True)

    events = orm.relationship ('Event')
    weights = orm.relationship ('Weight')

    def __init__ (self, name, password):
        """Store password in a trapdoor hash."""
        self.name = name
        self.hashPass = bcrypt.encrypt (password)

    def get_id (self):
        """Return the user name for Flask-login."""
        return self.name

    def setPass (self, password):
        """Modify password, with proper hygiene."""
        self.hashPass = bcrypt.encrypt (password)

    def checkPass (self, password):
        """Test proffered password against stored hash."""
        return bcrypt.verify (password, self.hashPass)

    def __repr__ (self):
        """Display a job owner."""
        return '<User {0:d} {1:s}>'.format (self.id, self.name)

class Weight (Base):
    """A body-weight sample."""
    __tablename__ = 'weight'

    # Define columns
    id = sql.Column (sql.Integer, primary_key=True)
    weight = sql.Column (sql.Float, nullable=False)
    unit = sql.Column (sql.Enum (_weightNames))
    timestamp = sql.Column (sql.DateTime (timezone=True),
                            nullable=False,
                            default=dt.datetime.now ())
    note = sql.Column (sql.Text, nullable=True)
    user_id = sql.Column (sql.ForeignKey ('users.id'))
    user = orm.relationship ('User', back_populates='weights')

    def __repr__ (self):
        """Text representation."""
        return '<Weight {0:d} at {1:s}: {2:f}>'.format (
            self.id, str (self.timestamp), self.weight)

class FoodLog (Base):
    """Log an event."""
    __tablename__ = 'foodLog'

    # Define columns
    id = sql.Column (sql.Integer, primary_key=True)
    kind = sql.Column (sql.Enum (EventTypes))
    quantity = sql.Column (sql.Float, nullable=True)
    unit = sql.Column (sql.Enum (_weightNames), nullable=True)
    timestamp = sql.Column (sql.DateTime (timezone=True),
                            default=dt.datetime.now ())
    note = sql.Column (sql.Text, nullable=True)
    user_id = sql.Column (sql.ForeignKey ('users.id'))
    user = orm.relationship ('User', back_populates='events')
