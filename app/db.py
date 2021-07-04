import mariadb
from logger import logger


class database:
    def __init__(self, db_address: str, db_name: str, db_username: str, db_password: str):
        self.address = db_address
        self.name = db_name
        self.username = db_username
        self.password = db_password

    def connect(self):
        return mariadb.connect(
        user=self.username,
        password=self.password,
        host=self.address,
        port=3306,
        database=self.name
        )

    def init_database(self):
        con = self.connect()
        cur = con.cursor()

        # Create table
        cur.execute('''CREATE TABLE IF NOT EXISTS submitter (
            flag VARCHAR(50) NOT NULL,
            tick INT NULL,
            status INT NULL DEFAULT 0,
            exploit VARCHAR(45) NOT NULL,
            statistics INT(1) DEFAULT 0,
            PRIMARY KEY (flag))''')

        # Save (commit) the changes
        con.commit()

        # Close connection
        con.close()

    def exec_query(self, query: str):
        con = self.connect()
        cur = con.cursor()
        cur.execute(query)
        res = cur.fetchall()
        con.commit()
        con.close()
        return res

    def insert_flags(self, flag: str, tick: int, exploit: str):
        duplicate = False

        try:
            con = self.connect()
            cursor = con.cursor()

            cursor.execute(
                "INSERT INTO submitter VALUES (?, ?, 0, ?, 0)", 
                (flag, tick, exploit))
            
            con.commit()
        except mariadb.IntegrityError:
            duplicate = True

        con.close()
        return duplicate


    def get_flags_to_send(self, limit: int):
        try:
            db = self.connect()
            cursor = db.cursor()

            query = "SELECT flag FROM submitter WHERE status=0 OR status=5"
            cursor.execute(query)

            flags = []
            i = 0
            for row in cursor:
                flags.append(row[0])
                i += 1
                if i >= limit and limit != -1:
                    break
            logger.info(f"{i} flags")
        except Exception as e:
            logger.exception("Si è sminchiato tutto leggendo....")

        db.close()
        return flags

    def mark_flag_as_sent(self, status, flags):
        try:
            db = self.connect()
            cursor = db.cursor()
            for i in range(len(flags)):
                cursor.execute(f"UPDATE submitter SET status={status[i]} WHERE flag='{flags[i]}'")
            db.commit()
        except Exception as e:
            logger.exception("Si è sminchiato tutto inserendo....")
            db.rollback()
        
        db.close()
        return
