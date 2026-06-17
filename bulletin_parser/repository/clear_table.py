from sqlalchemy import text

from bulletin_parser.core.models.db_helper import db_helper

def clear_table():
    with db_helper.get_session() as session:
        session.execute(
            text("TRUNCATE TABLE spimex_trading_results RESTART IDENTITY CASCADE"))

        session.commit()


if __name__ == '__main__':
    clear_table()