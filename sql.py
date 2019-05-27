import pandas as pd
from sqlalchemy import create_engine


class SQL:
    def __init__(self):
        self.engine = ""
        self.sortby = ""
        self.table = ""
        self.query = ""
        self.trans = []

    def db(self, database):
        self.engine = create_engine(f"sqlite:///{database}")
        return self

    def select(self, s):
        self.query = s
        return self

    def in_table(self, table):
        self.table = table
        return self

    def sort(self, by):
        self.sortby = "order by {by}"
        return self

    def transforms(self, tr):
        self.trans = tr
        return self

    def execute(self):
        data = pd.read_sql(f"select {self.query} from {self.table} {self.sortby}", self.engine)
        for key, func in self.trans:
            data[key] = data[key].apply(func)
        return data
