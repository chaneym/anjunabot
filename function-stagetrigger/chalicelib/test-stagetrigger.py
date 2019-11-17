import chalicelib.dbops as db
import chalicelib.models as m
from app import lambda_handler


def main():
    session = db.session_manager()
    for instance in session.query(m.MessageStage):
        lambda_handler({'row_id': instance.id})
        instance.transformed = 1
    db.commit_or_rollback(session)
    return


if __name__ == '__main__':
    main()
