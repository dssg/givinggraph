from givinggraph import config
from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker as sessionmakermaker, relationship

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

    news_articles = relationship("News_Article", backref='nonprofits')

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


news_article_companies_rel_table = Table('news_articles_companies_rel', Base.metadata,
                                         Column('news_articles_id', Integer, ForeignKey('news_articles.news_articles_id')),
                                         Column('companies_id', Integer, ForeignKey('companies.companies_id')))


class Company(Base):
    __tablename__ = 'companies'
    companies_id = Column(Integer, primary_key=True)
    ticker = Column(String)
    name = Column(String)
    exchange = Column(String)
    website = Column(String)
    industry = Column(String)
    sector = Column(String)
    summary = Column(String)

    def __init__(self, ticker, name, exchange, website, industry, sector, summary):
        self.ticker = ticker
        self.name = name
        self.exchange = exchange
        self.website = website
        self.industry = industry
        self.sector = sector
        self.summary = summary


class News_Article(Base):
    __tablename__ = 'news_articles'
    news_articles_id = Column(Integer, primary_key=True)
    nonprofits_id = Column(Integer, ForeignKey('nonprofits.nonprofits_id'))
    insert_time = Column(DateTime)
    url = Column(String)
    headline = Column(String)
    text = Column(String)

    companies = relationship('Company', secondary=news_article_companies_rel_table, backref='news_articles')

    def __init__(self, nonprofits_id, url, headline, text):
        self.nonprofits_id = nonprofits_id
        self.url = url
        self.headline = headline
        self.text = text


class Nonprofits_Similarity_By_Description(Base):
    __tablename__ = 'nonprofits_similarity_by_description2'
    nonprofits_similarity_by_description_id = Column(Integer, primary_key=True)
    charity1_id = Column(Integer, ForeignKey('nonprofits.nonprofits_id'))
    charity2_id = Column(Integer, ForeignKey('nonprofits.nonprofits_id'))
    similarity = Column(Float)

    def __init__(self, charity1_id, charity2_id, similarity):
        self.charity1_id = charity1_id
        self.charity2_id = charity2_id
        self.similarity = similarity
