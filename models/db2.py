
from sqlalchemy import create_engine, Column, Integer, String, MetaData

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


Base = declarative_base(metadata=MetaData())

class User(Base):
    __tablename__ = "person"
    name = Column("name", String(64), primary_key=True)
    password = Column("password", String(16), nullable=False)
    email = Column("email", String(50), nullable=False)


engine = create_engine('sqlite:///list_user.db', echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# user = User()
# user.name = 'vuduc'
# user.email = 'vuduc1711@gmail.com'
# user.password = 'asdheqe12387'
# session.add(user)
# session.commit()
# user1 = User()
# user1.name = 'minhtam'
# user1.email = 'minhtam.tmlk@gmail.com'
# user1.password = 'uqusdy21213'
# session.add(user1)
# session.commit()



def create_query_get():
    users = session.query(User).all()
    list_users = []
    for user in users:
        obj_user = {'name': user.name, 'password': user.password, 'email': user.email}
        list_users.append(obj_user)
    return list_users


def create_query_get_one(name):
    user = session.query(User).filter_by(name=name).all()
    return {'name': user[0].name, 'password': user[0].password, 'email': user[0].email}


def create_query_insert(name, password, email):
    new_user = User()
    new_user.name = name
    new_user.password = password
    new_user.email = email
    session.add(new_user)
    session.commit()


def create_query_update(name, new_pass, new_email):
    user = session.query(User).filter_by(name=name).first()
    user.password = new_pass
    user.email = new_email
    session.commit()


def create_query_delete(name):
    user = session.query(User).filter_by(name=name).first()
    session.delete(user)
    session.commit()


