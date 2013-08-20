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


class Nonprofits_Similarity_By_Tweets(Base):
    __tablename__ = 'nonprofits_similarity_by_tweets2'
    nonprofits_similarity_by_tweets_id = Column(Integer, primary_key=True)
    twitter_name1 = Column(Integer)
    twitter_name2 = Column(Integer)
    similarity = Column(Float)

    def __init__(self, twitter_name1, twitter_name2, similarity):
        self.twitter_name1 = twitter_name1
        self.twitter_name2 = twitter_name2
        self.similarity = similarity


class Nonprofit_Twitter_Attributes(Base):
    __tablename__ = 'nonprofit_twitter_attributes'
    nonprofit_twitter_attributes_id = Column(Integer, primary_key=True)
    nonprofit_id = Column(Integer)
    id = Column(String)
    label = Column(String)
    weighted_degree = Column(Integer)
    eccentricity = Column(Integer)
    closeness_centrality = Column(Float)
    betweenness_centrality = Column(Float)
    modularity_class = Column(Integer)
    authority = Column(Float)
    hub = Column(Float)
    clustering_coefficient = Column(Float)
    number_of_triangles = Column(Integer)
    weighted_clustering_coefficient = Column(Float)
    strength = Column(Integer)
    eigenvector_centrality = Column(Float)
    number_of_followers = Column(Integer)


class Tweet(Base):
    __tablename__ = 'nonprofits_tweets'
    nonprofits_tweets_id = Column(Integer, primary_key=True)
    twitter_name = Column(String)
    tweet_id = Column(String)
    date = Column(DateTime)
    text = Column(String)
    language = Column(String)
    retweet_count = Column(Integer)
    favorite_count = Column(Integer)
    mentions_ids = Column(String)
    mentions_names = Column(String)
    hashtags = Column(String)
    urls = Column(String)
    in_reply_to_screen_name = Column(String)
    in_reply_to_user_id = Column(String)
    in_reply_to_status_id = Column(Integer)

    def __init__(self, twitter_name, tweet_id, date, text, language, retweet_count, favorite_count, mentions_ids, mentions_names, hashtags, urls, in_reply_to_screen_name, in_reply_to_user_id, in_reply_to_status_id):
        self.twitter_name = twitter_name
        self.tweet_id = tweet_id
        self.date = date
        self.text = text
        self.language = language
        self.retweet_count = retweet_count
        self.favorite_count = favorite_count
        self.mentions_ids = mentions_ids
        self.mentions_names = mentions_names
        self.hashtags = hashtags
        self.urls = urls
        self.in_reply_to_screen_name = in_reply_to_screen_name
        self.in_reply_to_user_id = in_reply_to_user_id
        self.in_reply_to_status_id = in_reply_to_status_id
