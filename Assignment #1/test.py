from sqlalchemy import orm, create_engine, func, and_, tuple_
from password import PASSWORD
from sailors_query import Base, Sailor, Boat, Reservation

engine = create_engine('mysql+pymysql://kevinlin:' + PASSWORD + '@localhost:3306/sailorsdb')
conn = engine.connect()
Session = orm.sessionmaker()
Session.configure(bind=engine)
session = Session()


def assert_query(sql_query, orm_query):
    orm_list = []
    sql_list = []

    sql_items = conn.execute(orm_query).fetchall()
    for i, item in enumerate(sql_query):
        orm_list.append(item.__repr__())

    for i, item in enumerate(sql_items):
        sql_list.append(item)

    print(orm_list)
    print(sql_list)
    assert orm_list == sql_list

# Test a sample query result with orm
def test_query():
    test_query = "SELECT s.* FROM sailors as s,reserves as r, boats as b WHERE r.sid = s.sid AND b.bid = r.bid GROUP BY s.sid HAVING (s.sid, COUNT(s.sid)) IN (SELECT s.sid, COUNT(s.sid) FROM sailors as s,reserves as r, boats as b WHERE r.sid = s.sid AND b.bid = r.bid AND b.color = 'red' GROUP BY s.sid);"

    sub_query = session.query(Sailor.sid, func.count(Sailor.sid)).join(Reservation, Reservation.sid == Sailor.sid)\
        .join(Boat, and_(Reservation.bid == Boat.bid, Boat.color == 'red')).group_by(Sailor.sid).subquery()
    sql_query = session.query(Sailor).join(Reservation, Reservation.sid == Sailor.sid)\
        .join(Boat, Reservation.bid == Boat.bid).group_by(Sailor.sid).having(tuple_(Sailor.sid, func.count(Sailor.sid))
                                                                             .in_(sub_query)).all()
    assert_query(sql_query, test_query)


def test_object():
    sailor_query = "SELECT * FROM sailors"
    boat_query = "SELECT * FROM boats"
    reserves_query = "SELECT * FROM reserves"

    sailor_orm = session.query(Sailor).all()
    boat_orm = session.query(Boat).all()
    reserves_orm = session.query(Reservation).all()

    assert_query(sailor_orm, sailor_query)
    assert_query(boat_orm, boat_query)
    assert_query(reserves_orm, reserves_query)


