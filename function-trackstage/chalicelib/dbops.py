import os
from chalicelib.models import MessageStage
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_CON_STRING = os.environ['DB_CON_STRING']

write_engine = create_engine(DB_CON_STRING)
WriteSession = sessionmaker(bind=write_engine)


def get_or_create(model, **kwargs):
    session = WriteSession()
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        try:
            instance = model(**kwargs)
            session.add(instance)
            session.commit()
            return instance
        except Exception as e:
            session.rollback()
        finally:
            session.close()


def get_person(first_name):
    return get_or_create(first_name)


def message_stage(path, path_type, platform, person, comment, chat_id, chat_title):
    return get_or_create(MessageStage, path=path, path_type=path_type, platform=platform, person=person,
                         comment=comment, chat_id=chat_id, chat_title=chat_title)
