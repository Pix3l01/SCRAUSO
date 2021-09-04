import logging
from threading import Thread
from time import sleep
import requests
import json
import coloredlogs

class Logger:
    def __init__(self, log_level=logging.DEBUG, name=None, prefix='', suffix=''):
        if name is None:
            name = self.__class__.__module__ + '.' + self.__class__.__name__
        name = prefix + name + suffix

        self.logger = logging.getLogger(name)
        self.logger.addHandler(boskelHandler())
        coloredlogs.install(level=log_level, fmt='%(asctime)s,%(msecs)03d - %(name)s - %(levelname)s - %(message)s',
                            logger=self.logger)


class boskelHandler(logging.Handler):
    boskelBuffer = "["
    def __init__(self, level=logging.DEBUG):
        logging.Handler.__init__(self, level)
        thread = Thread(target=self.periodicUploader, args=())
        thread.start()

    def emit(self, record):
        data = record.__dict__.copy()
        msg = {'name': data['name'], 'message': str(data['msg']), 'level': data['levelname'],
               'created': data['created']}
        self.boskelBuffer += json.dumps(msg) + ","
    
    def upload(self):
        try:
            requests.post("http://boskel:7893/logs", timeout=1, headers={'Content-Type': 'application/json'},
                          data=self.boskelBuffer[:-1]+"]")
            self.boskelBuffer="["
        except Exception as ex:
            print("boskelHandler error, you can ignore this. " + str(ex), flush=True)
            # Clear buffer anyway, to prevent high memory usage
            self.boskelBuffer="["

    def periodicUploader(self):
        while True:
            self.upload()
            sleep(0.250)

logger = Logger(name="SCRAUSO").logger
loggerSubmitter = Logger(name="SCRAUSO-Submitter").logger
loggerReceiver = Logger(name="SCRAUSO-Receiver").logger
