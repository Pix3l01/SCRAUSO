import sqlite3
from requests import Request
import requests
import json

class senderInterface(object):
    def send(self):
        raise NotImplementedError()

class forcADsender(senderInterface):
    def __init__(self, db, token, url):
        self.db = db
        self.url = url
        self.headers = {"X-Team-Token" : token}


    def send(self):
        #again è per il constraint di mandare al max 100 flag alla volta
        again = 0
        try:
            db = sqlite3.connect(self.db)
            cursor = db.cursor()

            #query placeholder
            query = "SELECT flag FROM submitter WHERE status=0"
            cursor.execute(query)

            flags = []
            i = 0
            for row in cursor:
                flags.append(row)
                i += 1
                if i >= 100:
                    again = 1
                    break

        except:
            print("Si è sminchiato tutto leggendo....")
            db.close()
            return

        finally:
            db.close()

        resp = requests.put(url=self.url, data=json.dumps(flags), headers=self.headers)
        resp = json.loads(resp)
        try:
            db = sqlite3.connect(self.db)
            cursor = db.cursor()

            for r in resp:
                flag = r['flag']
                if ("accepted" in r['msg']):
                    status = 1
                if ("old" in r['msg']):
                    status = 2
                if ("invalid" in r['msg']):
                    status = 3
                if("already" in r['msg']):
                    status = 4
                cursor.execute(f"UPDATE submitter SET status={status} WHERE flag={flag}")

        except:
            print("Si è sminchiato tutto inserendo....")
            db.close()
            return

        finally:
            db.commit()
            db.close()

        if (again==1):
            self.send()
        print("Transazione effettuata con successo")
        return
