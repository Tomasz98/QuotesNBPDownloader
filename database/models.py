from sqlalchemy import create_engine, Column, Integer, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ExchangeRate(Base):
    __tablename__ = "exchange_rates"
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False, unique=True)
    eur_pln = Column(Numeric(10, 4), nullable=False)
    usd_pln = Column(Numeric(10, 4), nullable=False)
    chf_pln = Column(Numeric(10, 4), nullable=False)
    eur_usd = Column(Numeric(10, 4), nullable=False)
    chf_usd = Column(Numeric(10, 4), nullable=False)


engine = create_engine("postgresql://user:password@db/mydatabase")
Base.metadata.create_all(engine)
