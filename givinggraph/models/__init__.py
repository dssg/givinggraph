from givinggraph import config
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker as sessionmakermaker

host = config.read_config('database', 'host')
db_name = config.read_config('database', 'database')
user = config.read_config('database', 'user')
password = config.read_config('database', 'pass')
connection_string = 'mysql+mysqldb://{0}:{1}@{2}/{3}'.format(user, password, host, db_name)
engine = create_engine(connection_string, encoding='latin1', convert_unicode=True)
# yep, it's latin1. Check it:
# mysql -h host-stuff-here.rds.amazonaws.com -u ourusername -p
# SHOW DATABASES;
# USE THEDATABASEWITHSTUFFINIT;
# SHOW VARIABLES LIKE "character_set_database";
sessionmaker = sessionmakermaker(bind=engine)
DBSession = sessionmaker()

Base = declarative_base()


class Nonprofit(Base):
    # __table__ = Table('tweets', metadata, autoload=True)
    __tablename__ = 'nonprofits'
    nonprofits_id = Column(Integer, primary_key=True)
    name = Column(String)
    ein = Column(String)
    ntee_code = Column(String)
    mission_statement = Column(String)
    description = Column(String)
    twitter_id = Column(String)
    twitter_name = Column(String)
    city = Column(String)
    state = Column(String)
    ZIP = Column(String)

    def __init__(self, name, ein, ntee_code, mission_statement, description, twitter_id, twitter_name, city, state, ZIP):
        self.name = name
        self.ein = ein
        self.ntee_code = ntee_code
        self.mission_statement = mission_statement
        self.description = description
        self.twitter_id = twitter_id
        self.twitter_name = twitter_name
        self.city = city
        self.state = state
        self.ZIP = ZIP
