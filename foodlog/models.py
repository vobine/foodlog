import datetime as dt
import sqlalchemy as sql
import sqlalchemy.orm as orm
import sqlalchemy.ext.declarative as sqldcl
import sqlalchemy.event as sqlevt
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
    name = sql.Column (sql.String (30))
    hashPass = sql.Column (sql.String (150), nullable=True)

    events = orm.relationship ('FoodLog')
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
    timestamp = sql.Column (sql.DateTime (timezone=True),
                            nullable=False,
                            default=dt.datetime.now ())
    note = sql.Column (sql.Text, nullable=True)
    user_id = sql.Column (sql.ForeignKey ('users.id'))
    user = orm.relationship ('User', back_populates='weights')

    def __repr__ (self):
        """Text representation."""
        return '<Weight {0:d} at {1:s}: {2:f} kilograms>'.format (
            self.id, str (self.timestamp), self.weight / 1000)

class Kind (Base):
    """Event types"""
    __tablename__ = 'kinds'

    # Define columns
    id = sql.Column (sql.String (4), primary_key=True)
    name = sql.Column (sql.String (20), nullable=False)
    notes = sql.Column (sql.Text, nullable=True)

    events = orm.relationship ('FoodLog', back_populates='kind')

    def __repr__ (self):
        """Textual representation."""
        return '<Event {0:s}>'.format (self.id)

class FoodLog (Base):
    """Log an event."""
    __tablename__ = 'foodLog'

    # Define constants
    units = dict (weight='grams', 
                  volume='liters', 
                  length='meters',
                  count='count', 
                  servings='count')
    dimensions = frozenset (units.keys ())

    # Define columns
    id = sql.Column (sql.Integer, primary_key=True)
    quantity = sql.Column (sql.Float, nullable=True)
    dimension = sql.Column (sql.Enum (* dimensions), nullable=True)
    timestamp = sql.Column (sql.DateTime (timezone=True),
                            default=dt.datetime.now ())
    notes = sql.Column (sql.Text, nullable=True)

    kind_id = sql.Column (sql.ForeignKey ('kinds.id'))
    kind = orm.relationship ('Kind', back_populates='events')

    user_id = sql.Column (sql.ForeignKey ('users.id'))
    user = orm.relationship ('User', back_populates='events')


def init_db (url, verbose=False):
    """Initialize connection to database."""
    global session
    engine = sql.create_engine (url, echo=verbose)
    session = orm.scoped_session (
        orm.sessionmaker (autocommit=False,
                          autoflush=False,
                          bind=engine))
    Base.query = session.query_property ()
    Base.metadata.create_all (bind=engine)

@sqlevt.listens_for (Kind.__table__, 'after_create')
def initialize_kinds (*args, **kwargs):
    global session
    session.add_all ( [
        Kind (id='MF', name='Medifast meal'),
        Kind (id='H2O', name='Water'),
        Kind (id='Sup', name='Supplements'),
        Kind (id='Lean', name='Lean protein'),
        Kind (id='Grn', name='Green vegetables'),
        Kind (id='L/G', name='Lean and/or green'),
        Kind (id='Ex', name='Exercise'),
        Kind (id='Off', name='Off-plan food'),
        Kind (id='Fat', name='Healthy fat'),
    ] )
    session.commit ()
