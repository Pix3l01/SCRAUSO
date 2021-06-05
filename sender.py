import sqlite3

class senderInterface(object):
    def send(self):
        raise NotImplementedError()

class forcADsender(senderInterface):
    def __init__(self, db):
        self.db=db

    def send(self):
        try:
            db = sqlite3.connect(db)
            cursor = db.cursor()

            #query placeholder
            query="SELECT flag FROM flags WHERE used=0"
            cursor.execute(query)

            flags = []
            for row in cursor:
                flags.append(cursor.fetchone())

        except Exception as e:
            print("Si è sminchiato tutto")

        finally:
            db.close()
