import requests
import json
from logger import loggerSubmitter as logger
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
        logger.info("Sending...")
        flags = self.db.get_flags_to_send(100)
        # again è per il constraint di mandare al max 100 flag alla volta
        again = len(flags) >= 100

        resp = requests.put(url=self.url, data=json.dumps(flags), headers=self.headers)
        try:
            resp = json.loads(resp.text)
        except Exception as e:
            logger.exception(resp.text)
            logger.error("No response...")
            return

        status = []

        if type(resp) is not list or type(resp[0]) is not dict:
            raise Exception("resp type is wrong", resp)
        for r in resp:
            flag = r['flag']
            #print(flag)
            if ("accepted" in r['msg']):
                status.append(1)
            elif ("old" in r['msg']):
                status.append(2)
            elif ("invalid" in r['msg']):
                status.append(3)
            elif ("already" in r['msg']):
                status.append(4)
            else:
                logger.info("GS says: --> " + r['msg'] + "for flag=" + flag)
                status.append(5)

        self.db.mark_flag_as_sent(status, flags)

        if again:
            self.send()
        logger.info("Transazione effettuata con successo")
        return


class ncsender(senderInterface):
    def __init__(self, db, token, ip, port):
        self.db = db
        self.ip = ip
        self.port = port
        self.token = token

    def send(self):
        logger.info("Sending...")
        flags = self.db.get_flags_to_send(-1)

        status = []
        io = remote(self.ip, self.port)
        io.sendline(self.token)
        ans = io.recvline()
        if b"Invalid" in ans:
            logger.error(ans)
            return

        for f in flags:
            io.sendline(f)
            msg = io.recvline()
            #print(f)
            if (b"accepted" in msg):
                status.append(1)
            elif (b"old" in msg):
                status.append(2)
            elif (b"invalid" in msg):
                status.append(3)
            elif (b"already" in msg):
                status.append(4)
            else:
                logger.info(b"GS says: --> " + msg + b" \n for flag=" + f.encode())
                status.append(5)

        self.db.mark_flag_as_sent(status, flags)

class faustSender(senderInterface):
    def __init__(self, db, ip, port):
        self.db = db
        self.ip = ip
        self.port = port

    def send(self):
        logger.info("Sending...")
        flags = self.db.get_flags_to_send(-1)

        status = []
        io = remote(self.ip, self.port)
        banner = io.recv()

        for f in flags:
            io.sendline(f)
            msg = io.recvline()
            #print(f)
            if (b"Thank you" in msg):
                status.append(1)
            elif (b"expired" in msg):
                status.append(2)
            elif (b"not recognized" in msg or b"No such Flag" in msg):
                status.append(3)
            elif (b"once" in msg):
                status.append(4)
            else:
                logger.info(b"GS says: --> " + msg + b" \n for flag=" + f.encode())
                status.append(5)

        self.db.mark_flag_as_sent(status, flags)
