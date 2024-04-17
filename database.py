from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:test_0830@localhost:3306/wallpapersDB'
SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://admin:Rds_0830@wallpaperdb.c1awemqk6d51.us-east-1.rds.amazonaws.com:3306/wallpapersDB'


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()