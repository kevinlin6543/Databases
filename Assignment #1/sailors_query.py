from sqlalchemy import create_engine
from sqlalchemy import orm, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Column, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import backref, relationship
from sqlalchemy import PrimaryKeyConstraint
from password import PASSWORD

Base = declarative_base()


class Sailor(Base):
    __tablename__ = 'sailors'

    sid = Column(Integer, primary_key=True)
    sname = Column(String)
    rating = Column(Integer)
    age = Column(Integer)

    def __repr__(self):
        return "<Sailor(id=%s, name='%s', rating=%s)>" % (self.sid, self.sname, self.age)


class Boat(Base):
    __tablename__ = 'boats'

    bid = Column(Integer, primary_key=True)
    bname = Column(String)
    color = Column(String)
    length = Column(Integer)

    reservations = relationship('Reservation',
                                backref=backref('boat', cascade='delete'))

    def __repr__(self):
        return "<Boat(id=%s, name='%s', color=%s)>" % (self.bid, self.bname, self.color)


class Reservation(Base):
    __tablename__ = 'reserves'
    __table_args__ = (PrimaryKeyConstraint('sid', 'bid', 'day'), {})

    sid = Column(Integer, ForeignKey('sailors.sid'))
    bid = Column(Integer, ForeignKey('boats.bid'))
    day = Column(DateTime)

    sailor = relationship('Sailor')

    def __repr__(self):
        return "<Reservation(sid=%s, bid=%s, day=%s)>" % (self.sid, self.bid, self.day)


engine = create_engine('mysql+pymysql://kevinlin:' + PASSWORD + '@localhost:3306/sailorsdb')
conn = engine.connect()
Session = orm.sessionmaker()
Session.configure(bind=engine)
session = Session()



sql_query = session.query(func.avg(Sailor.age)).filter_by(rating=10).group_by(Sailor.age).first()
print(sql_query)

sql_query = session.query(Sailor).outerjoin(Reservation, Sailor.sid == Reservation.sid).filter_by(sid=None).join(Boat, Reservation.bid==Boat.bid and Boat.color=='red')
print(sql_query)

#print(conn.execute("SELECT * from sailors").fetchall())

print(conn.execute("SELECT t.bid, t.sid, MAX(count1) FROM (SELECT r.bid as bid, r.sid as sid, COUNT(r.bid) as count1 FROM reserves as r, sailors as s WHERE r.sid = s.sid GROUP BY r.bid, r.sid ORDER BY count1 DESC) as t GROUP BY t.bid ORDER BY t.bid;").fetchall())
