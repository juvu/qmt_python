from datetime import datetime

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, DateTime
# 使用SQLAlchemy的DeclarativeBase来定义模型
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship

Base = declarative_base()
metadata = MetaData()
DATABASE_URL = 'postgresql://postgres:dirtydan@120.26.202.151:5432/demo1'


#

class ChatGroup(Base):
    __tablename__ = 'chat_groups'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class Stock(Base):
    __tablename__ = 'stocks'
    name = Column(String, primary_key=True)


class ShareRecord(Base):
    __tablename__ = 'share_records'
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('chat_groups.id'), nullable=False)
    stock_name = Column(String, ForeignKey('stocks.name'), nullable=False)
    share_time = Column(DateTime, default=datetime.utcnow)

    chat_group = relationship("ChatGroup")
    stock = relationship("Stock")


class tjItem(Base):
    __tablename__ = 'tjItem'
    id = Column(Integer, primary_key=True)
    qm = Column(String)
    info = Column(String)

class WatchCode(Base):
    __tablename__ = 'WatchCode'
    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True)
    market = Column(String)
    create_time = Column(DateTime, default=datetime.utcnow)

class WaitBuyList(Base):
    __tablename__ = 'WaitBuyList'
    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True)
    market = Column(String)
    create_time = Column(DateTime, default=datetime.utcnow)


engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db = SessionLocal()


def get_items(skip: int = 0, limit: int = 100):
    return db.query(tjItem).offset(skip).limit(limit).all()


def create(obj):
    try:
        db.add(obj)
        db.commit()
        db.refresh(obj)
    except Exception as e:
        db.rollback()
        print(e)
    return obj

def update(obj):
    return db.query(obj).all()


def read(obj):
    return db.query(obj).all()


def get_db():
    return db


if __name__ == '__main__':
    Base.metadata.create_all(engine)
