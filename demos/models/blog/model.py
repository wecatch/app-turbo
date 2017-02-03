from datetime import datetime

from .base import Base
from sqlalchemy import Column, Integer, Text, VARCHAR, BLOB, DateTime


class Blog(Base):

    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(BLOB, nullable=False)
    text = Column(BLOB, nullable=False)
    dig_count = Column(Integer)
    uid = Column(Integer)
    comment_count = Column(Integer)
    atime = Column(DateTime, default=datetime.now, nullable=False)
