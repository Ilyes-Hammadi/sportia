from sqlalchemy import Column, Integer, String, ForeignKey, func, DateTime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(250))
    created = Column(DateTime, default=func.now())


class Sport(Base):
    __tablename__ = 'sport'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(250))

    created = Column(DateTime, default=func.now())

    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)


engine = create_engine('sqlite:///sportia.db')

Base.metadata.create_all(engine)
