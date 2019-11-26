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
from operator import add, sub

STARTING_BID = 101

Base = declarative_base()
engine = create_engine('mysql+pymysql://kevinlin:' + PASSWORD + '@localhost:3306/sailorsdbnew')
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

    def __repr__(self):
        return "<Sailor(id=%s, name='%s', rating=%s, age=%s)>" % (self.sid, self.sname, self.rating, self.age)

class Boat(Base):
    __tablename__ = 'boats'

    bid = Column(Integer, primary_key=True)
    bname = Column(String)
    color = Column(String)
    length = Column(Integer)
    cost = Column(Integer)
    rate = Column(Integer)

    reservations = relationship('Reservation',
                                backref=backref('boat', cascade='delete'))

    def __repr__(self):
        return "<Boat(id=%s, name='%s', color=%s, length=%s, cost=$%s, rate=$%s/hour)>" % (self.bid, self.bname, self.color, self.length, self.cost, self.rate)


class Reservation(Base):
    __tablename__ = 'reserves'
    __table_args__ = (PrimaryKeyConstraint('sid', 'bid', 'day'), {})

    sid = Column(Integer, ForeignKey('sailors.sid'))
    bid = Column(Integer, ForeignKey('boats.bid'))
    day = Column(DateTime)
    hour = Column(Integer)

    sailor = relationship('Sailor')

    def __repr__(self):
        return "<Reservation(sid=%s, bid=%s, day=%s, hours=%s)>" % (self.sid, self.bid, self.day, self.hour)


class Repairs(Base):
    __tablename__ = 'repairs'
    __table_args__ = (PrimaryKeyConstraint('bid', 'cost'), {})
    bid = Column(Integer, ForeignKey('boats.bid'))
    cost = Column(Integer)

    sailor = relationship('Boat')
    def __repr__(self):
        return "<Repairs(bid=%s, cost=%s)>" % (self.bid, self.cost)


def profit_tracker():
    boat_costs = session.query(Boat.cost).all()

    # Money Earned from aggregating the time each boat is reserved and the rate
    earned_query = session.query(func.sum(Boat.rate*Reservation.hour)).join(Reservation, Boat.bid==Reservation.bid).group_by(Boat.bid).order_by(Boat.bid).all()

    # Cost of Repairs for each boat
    repair_query = session.query(Boat.bid, func.sum(Repairs.cost)).outerjoin(Repairs, Repairs.bid==Boat.bid).group_by(Boat.bid).order_by(Boat.bid).all()

    repair_list = []
    cost_list = []
    earned_list = []
    for i in range(len(repair_query)):
        value = repair_query[i][1]
        if value == None:
            repair_list.append(0)
        else:
            repair_list.append(int(value))

    for i in range(len(boat_costs)):
        value = boat_costs[i][0]
        cost_list.append(int(value))

    for i in range(len(earned_query)):
        value = earned_query[i][0]
        earned_list.append(int(value))

    total_cost = list(map(add, repair_list, cost_list))
    boat_profit = list(map(sub, earned_list, total_cost))

    for i in range(len(boat_profit)):
        print("Boat ID: %d has a profit of $%d" %(STARTING_BID+i, boat_profit[i]))

profit_tracker()