import sqlite3


class database:
    def __init__(self, db_path: str):
        self.path = db_path

    def init_database(self):
        con = sqlite3.connect(self.path)
        cur = con.cursor()

        # Create table
        cur.execute('''CREATE TABLE IF NOT EXISTS 'submitter' (
            'flag' VARCHAR(50) NOT NULL,
            'tick' INT NULL,
            'status' INT NULL DEFAULT 0,
            'exploit' VARCHAR(45) NOT NULL,
            'statistics' INT(1) DEFAULT 0,
            PRIMARY KEY ('flag'))''')

        # Save (commit) the changes
        con.commit()

        # Close connection
        con.close()

    def exec_query(self, query: str):
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        res = cur.execute(query)
        con.commit()
        con.close()
        return res
