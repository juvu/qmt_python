from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
# 使用SQLAlchemy的DeclarativeBase来定义模型
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

Base = declarative_base()

DATABASE_URL ='postgresql://postgres:123456@localhost:5432/test'

class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    qm = Column(String, index=True)
    info = Column(String, index=True)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Item).offset(skip).limit(limit).all()

def create_tj(db: Session, item: Item):
    db.add(item)
    db.commit()
    db.refresh(item)
    return item