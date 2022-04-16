from datetime import date as d

from sqlalchemy import Column, Integer, Date
from sqlalchemy import create_engine
from sqlalchemy import func, desc
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///databases/schedules.db"

SchedulesEngine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SchedulesSession = sessionmaker(autocommit=False, autoflush=False, bind=SchedulesEngine)

SchedulesBase = declarative_base()


class Schedule(SchedulesBase):
    __tablename__ = "schedules"
    id = Column(Integer, primary_key=True)
    start_date = Column(Date)
    timestamp = Column(Integer)

    @classmethod
    def get_actual_dates_and_timestamps(cls, date: d):
        with SchedulesSession.begin() as session:
            schedules_timestamps = session.query(
                cls.start_date, func.max(cls.timestamp)
            ).filter(
                cls.start_date >= date
            ).group_by(
                cls.start_date
            ).order_by(
                desc(cls.start_date), cls.timestamp
            ).all()
        return schedules_timestamps