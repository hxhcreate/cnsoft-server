from contextlib import contextmanager

from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

from ..models import db


class DbUtil:

    def get_session(self, bind='admin'):
        engine = db.get_engine(app=db.get_app(), bind=bind)
        Session = sessionmaker(bind=engine)
        return Session()

    @contextmanager
    def auto_commit(self, bind='admin'):

        try:
            self.session = self.get_session(bind=bind)
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
        finally:
            self.session.close()

    """
       用于执行一次查询的数据库查询操作封装
    """

    def Update(self, sql='', params={}):
        session = self.session
        if sql:
            stmt = text(sql)
            if params:
                session.execute(stmt, params)
            else:
                session.execute(stmt)
        else:
            print("SQL为空!")

    def Select(self, sql='', params={}):
        resList = []
        session = self.session
        if sql:
            stmt = text(sql)
            if params:
                for record in session.execute(stmt, params):
                    # print(type(record))
                    rowDict = dict((zip(record.keys(), record)))
                    resList.append(rowDict)
                print(resList)
                return resList
            else:
                for record in session.execute(stmt):
                    # print(type(record))
                    rowDict = dict((zip(record.keys(), record)))
                    resList.append(rowDict)
                print(resList)
                return resList
        else:
            print("SQL为空!")

    def __del__(self):
        self.session.close()