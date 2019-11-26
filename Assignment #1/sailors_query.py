from sqlalchemy import create_engine
from sqlalchemy import orm, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Column, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import backref, relationship, sessionmaker
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy import and_, tuple_, desc
from sqlalchemy import distinct
from password import PASSWORD

Base = declarative_base()
engine = create_engine('mysql+pymysql://kevinlin:' + PASSWORD + '@localhost:3306/sailorsdb')
conn = engine.connect()
Session = orm.sessionmaker()
Session.configure(bind=engine)
session = Session()

class Sailor(Base):
    __tablename__ = 'sailors'

    sid = Column(Integer, primary_key=True)
    sname = Column(String)
    rating = Column(Integer)
    age = Column(Integer)

    def __str__(self):
        return "<Sailor(id=%s, name='%s', rating=%s, age=%s)>" % (self.sid, self.sname, self.rating, self.age)

    def __repr__(self):
        return self.sid, self.sname, self.rating, self.age

class Boat(Base):
    __tablename__ = 'boats'

    bid = Column(Integer, primary_key=True)
    bname = Column(String)
    color = Column(String)
    length = Column(Integer)

    reservations = relationship('Reservation',
                                backref=backref('boat', cascade='delete'))

    def __str__(self):
        return "<Boat(id=%s, name='%s', color=%s, length=%s)>" % (self.bid, self.bname, self.color, self.length)

    def __repr__(self):
        return self.bid, self.bname, self.color, self.length

class Reservation(Base):
    __tablename__ = 'reserves'
    __table_args__ = (PrimaryKeyConstraint('sid', 'bid', 'day'), {})

    sid = Column(Integer, ForeignKey('sailors.sid'))
    bid = Column(Integer, ForeignKey('boats.bid'))
    day = Column(DateTime)

    sailor = relationship('Sailor')

    def __str__(self):
        return "<Reservation(sid=%s, bid=%s, day=%s)>" % (self.sid, self.bid, self.day)

    def __repr__(self):
        return self.sid, self.bid, self.day


# Sample queries based off the SQL query created initially

def sample_orm_queries():
    sub_query = session.query(Sailor.sid, func.count(Sailor.sid)).join(Reservation, Reservation.sid == Sailor.sid).join(
        Boat, and_(Reservation.bid == Boat.bid, Boat.color == 'red')).group_by(Sailor.sid).subquery()
    sql_query = session.query(Sailor).join(Reservation, Reservation.sid == Sailor.sid).join(Boat,
                                                                                            Reservation.bid == Boat.bid).group_by(
        Sailor.sid).having(tuple_(Sailor.sid, func.count(Sailor.sid)).in_(sub_query)).all()

    sql_query = session.query(Boat.bid, Boat.bname, func.count(Reservation.bid).label('total')).join(Reservation,
                                                                                                     Reservation.bid == Boat.bid).order_by(
        desc('total')).group_by(Boat.bid).first()

    sub_query = session.query(Reservation).join(Boat, and_(Reservation.bid == Boat.bid, Boat.color == 'red')).subquery()
    sql_query = session.query(Sailor).outerjoin(sub_query, Sailor.sid == sub_query.c.sid).filter_by(sid=None).all()

    sql_query = session.query(func.avg(Sailor.age)).filter_by(rating=10).group_by(Sailor.age).first()