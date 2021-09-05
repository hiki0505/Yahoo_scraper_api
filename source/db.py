import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
import config

Base = declarative_base()


class Company(Base):
    __tablename__ = "companies"

    id_ = sa.Column('id', sa.Integer(), primary_key=True)
    company = sa.Column('company', sa.String(), index=True, nullable=False)
    date = sa.Column('date', sa.Date())
    open = sa.Column('open', sa.Float())
    high = sa.Column('high', sa.Float())
    low = sa.Column('low', sa.Float())
    close = sa.Column('close', sa.Float())
    adj = sa.Column('adj', sa.Float())
    volume = sa.Column('volume', sa.Integer())

    def __repr__(self):
        return f'Company(title="{self.company}", date={self.date})'


engine = sa.create_engine(config.DATABASE, echo=True)
Base.metadata.create_all(bind=engine)
