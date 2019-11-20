import chalicelib.data_warehouse as dw
import chalicelib.models as m
from app import lambda_handler


def main():
    session = dw.get_session()
    row_ids = []
    for instance in session.query(m.MessageStage):
        row_ids.append(instance.id)
    session.close()
    for row_id in row_ids:
        lambda_handler({'row_id': row_id})
    return


if __name__ == '__main__':
    main()
