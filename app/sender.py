import sqlite3
import requests
import json
from pwn import *


class senderInterface(object):
    def send(self):
        raise NotImplementedError()


class forcADsender(senderInterface):
    def __init__(self, db, token, url):
        self.db = db
        self.url = url
        self.headers = {"X-Team-Token": token}

    def send(self):
        print("Sending...")
        # again è per il constraint di mandare al max 100 flag alla volta
        again = 0
        try:
            db = sqlite3.connect(self.db)
            cursor = db.cursor()

            query = "SELECT flag FROM submitter WHERE status=0 OR status=99"
            cursor.execute(query)

            flags = []
            i = 0
            for row in cursor:
                flags.append(row[0])
                i += 1
                if i >= 100:
                    again = 1
                    break
            print(f"{i} flags")
        except Exception as e:
            print("Si è sminchiato tutto leggendo....")
            print(e)
            db.close()
            return

        db.close()

        resp = requests.put(url=self.url, data=json.dumps(flags), headers=self.headers)
        try:
            resp = json.loads(resp.text)
        except Exception as e:
            print(resp.text)
            print(e)
            print("No response...")
            return
        try:
            db = sqlite3.connect(self.db)
            cursor = db.cursor()
            if type(resp) is not list or type(resp[0]) is not dict:
                raise Exception("resp type is wrong", resp)
            for r in resp:
                flag = r['flag']
                # print(flag)
                if ("accepted" in r['msg']):
                    status = 1
                elif ("old" in r['msg']):
                    status = 2
                elif ("invalid" in r['msg']):
                    status = 3
                elif ("already" in r['msg']):
                    status = 4
                else:
                    print("GS says: --> " + r['msg'] + "for flag=" + flag)
                    status = 99
                cursor.execute(f"UPDATE submitter SET status=? WHERE flag='{flag}'", (status,))

            db.commit()
            db.close()

        except Exception as e:
            print("Si è sminchiato tutto inserendo....")
            print(e)
            db.rollback()
            db.close()
            return

        if (again == 1):
            self.send()
        print("Transazione effettuata con successo")
        return


class ncsender(senderInterface):
    def __init__(self, db, token, ip, port):
        self.db = db
        self.ip = ip
        self.port = port
        self.token = token

    def send(self):
        print("Sending...")
        try:
            db = sqlite3.connect(self.db)
            cursor = db.cursor()

            query = "SELECT flag FROM submitter WHERE status=0"
            cursor.execute(query)

            flags = []
            i = 0
            for row in cursor:
                flags.append(row[0])
                i += 1
            print(f"{i} flags")
            db.close()

        except Exception as e:
            print("Si è sminchiato tutto leggendo....")
            print(e)
            db.close()
            return

        status = []
        io = remote(self.ip, self.port)
        io.sendline(self.token)
        ans = io.recvline()
        if b"Invalid" in ans:
            print(ans)
            return

        for f in flags:
            io.sendline(f)
            msg = io.recvline()
            # print(f)
            if (b"accepted" in msg):
                status.append(1)
            elif (b"old" in msg):
                status.append(2)
            elif (b"invalid" in msg):
                status.append(3)
            elif (b"already" in msg):
                status.append(4)
            else:
                print(b"GS says: --> " + msg + b" \n for flag=" + f.encode())
                status.append(99)
        try:
            db = sqlite3.connect(self.db)
            cursor = db.cursor()
            # TODO: transform in cur.executemany
            for i in range(len(flags)):
                cursor.execute(f"UPDATE submitter SET status=? WHERE flag='{flags[i]}'", (status[i],))
            db.commit()
            db.close()
            return

        except Exception as e:
            print("Si è sminchiato tutto inserendo....")
            print(e)
            db.rollback()
            db.close()
            return


class faustSender(senderInterface):
    def __init__(self, db, ip, port):
        self.db = db
        self.ip = ip
        self.port = port

    def send(self):
        print("Sending...")
        try:
            db = sqlite3.connect(self.db)
            cursor = db.cursor()

            query = "SELECT flag FROM submitter WHERE status=0"
            cursor.execute(query)

            flags = []
            i = 0
            for row in cursor:
                flags.append(row[0])
                i += 1
            print(f"{i} flags")
            db.close()

        except Exception as e:
            print("Si è sminchiato tutto leggendo....")
            print(e)
            db.close()
            return

        status = []
        io = remote(self.ip, self.port)
        banner = io.recv()

        for f in flags:
            io.sendline(f)
            msg = io.recvline()
            # print(f)
            if (b"Thank you" in msg):
                status.append(1)
            elif (b"expired" in msg):
                status.append(2)
            elif (b"not recognized" in msg or b"No such Flag" in msg):
                status.append(3)
            elif (b"once" in msg):
                status.append(4)
            else:
                print(b"GS says: --> " + msg + b" \n for flag=" + f.encode())
                status.append(99)

        try:
            db = sqlite3.connect(self.db)
            cursor = db.cursor()
            # TODO: transform in cur.executemany
            for i in range(len(flags)):
                cursor.execute(f"UPDATE submitter SET status=? WHERE flag='{flags[i]}'", (status[i],))
            db.commit()
            db.close()
            return

        except Exception as e:
            print("Si è sminchiato tutto inserendo....")
            print(e)
            db.rollback()
            db.close()
            return


class ctfzone(senderInterface):
    def __init__(self, db, token, url):
        self.db = db
        self.url = url
        self.headers = {"Authorization": token, "Content-Type": "application/json"}

    def send(self):
        print("Sending...")
        try:
            db = sqlite3.connect(self.db)
            cursor = db.cursor()

            query = "SELECT flag FROM submitter WHERE status=0 OR status=99"
            cursor.execute(query)

            flags = []
            for row in cursor:
                flags.append(row[0])
        except Exception as e:
            print("Si è sminchiato tutto leggendo....")
            print(e)
            db.close()
            return

        db.close()

        for flag in flags:
            data = {"flag": flag}
            r = requests.post(url=self.url, data=json.dumps(data), headers=self.headers)
            print(r.text)
            try:
                r = json.loads(r.text)
            except Exception as e:
                print(r.text)
                print(e)
                print("No response...")
                return
            print(r)
            try:
                db = sqlite3.connect(self.db)
                cursor = db.cursor()
                # print(flag)
                if (r['success']):
                    status = 1
                elif ("expired" in r['error']['msg']):
                    status = 2
                elif ("Not a flag" in r['error']['msg']):
                    status = 3
                elif ("already" in r['error']['msg']):
                    status = 4
                else:
                    print("GS says: --> " + r['error']['msg'] + "for flag=" + flag)
                    status = 99
                cursor.execute(f"UPDATE submitter SET status=? WHERE flag='{flag}'", (status,))
            except Exception as e:
                print("Si è sminchiato tutto inserendo....")
                print(e)
                db.rollback()
                db.close()
                return

            db.commit()
            db.close()


class saarSender(senderInterface):
    def __init__(self, db, host, port):
        self.db = db
        self.host = host
        self.port = port

    def send(self):
        print("Retrieving flags from DB...")
        try:
            db = sqlite3.connect(self.db)
            cursor = db.cursor()

            query = "SELECT flag FROM submitter WHERE status=0 OR status=99"
            cursor.execute(query)

            flags = []
            i = 0
            for row in cursor:
                flags.append(row[0])
                i += 1
            print(f"{i} flags")
            db.close()

        except Exception as e:
            print("Si è sminchiato tutto leggendo....")
            print(e)
            db.close()
            return

        status = []
        io = remote(self.host, self.port)
        banner = io.recv()

        for f in flags:
            io.sendline(f)
            msg = io.recvline()
            if b"[OK]" in msg:
                status.append(1)
            elif b"Expired" in msg:
                status.append(2)
            elif b"Invalid" in msg:
                status.append(3)
            elif b"Already" in msg:
                status.append(4)
            elif b"NOP" in msg:
                status.append(5)
            elif b"own" in msg:
                status.append(6)
            else:
                print(b"GS says: --> " + msg + b" \n for flag=" + f.encode())
                status.append(99)

        try:
            db = sqlite3.connect(self.db)
            cursor = db.cursor()
            # TODO: transform in cur.executemany
            for i in range(len(flags)):
                cursor.execute(f"UPDATE submitter SET status=? WHERE flag='{flags[i]}'", (status[i],))
            db.commit()
            db.close()
            return

        except Exception as e:
            print("Si è sminchiato tutto inserendo....")
            print(e)
            db.rollback()
            db.close()
            return
