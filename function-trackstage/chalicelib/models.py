from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class MessageStage(Base):
    __tablename__ = 'message_stage'

    id = Column(Integer, primary_key=True)
    path = Column(String)
    path_type = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    text = Column(String)
    chat_id = Column(String)
    chat_title = Column(String)
    platform = Column(String)
