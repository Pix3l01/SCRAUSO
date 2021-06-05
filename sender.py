import sqlite3
from requests import Request
import requests
import json

male = 1
bene = 0

class senderInterface(object):
    def send(self):
        raise NotImplementedError()

class forcADsender(senderInterface):
    def __init__(self, db, token, url):
        self.db = db
        self.url = url
        self.headers = {"X-Team-Token" : token}


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
            db.close()
            return male

        finally:
            db.close()

        resp = requests.put(url=self.url, data=json.dumps(flags), headers=self.headers)

        stats(json.loads(resp))

        return bene

    def stats(resp):
        #coming soon
