import sqlite3
from requests import Request
import requests
import json

class senderInterface(object):
    def send(self):
        raise NotImplementedError()

class forcADsender(senderInterface):
    def __init__(self, db, token):
        self.db = db
        self.token = token

    def send(self):
        try:
            db = sqlite3.connect(self.db)
            cursor = db.cursor()

            #query placeholder
            query = "SELECT flag FROM submitter WHERE used=0"
            cursor.execute(query)

            flags = []
            for row in cursor:
                flags.append(cursor.fetchone())

        except Exception as e:
            print("Si è sminchiato tutto....")

        finally:
            db.close()

        jason = json.dumps(flags)
        resp = requests.put(url=self.url, data=jason, headers=self.headers)

        stats(json.loads(resp))

    def stats(resp):
        #coming soon
