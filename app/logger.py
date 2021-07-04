import logging
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
    def __init__(self, level=logging.DEBUG):
        logging.Handler.__init__(self, level)

    def emit(self, record):
        data = record.__dict__.copy()
        msg = {'name': data['name'], 'message': str(data['msg']), 'level': data['levelname'],
               'created': data['created']}
        try:
            requests.post("http://127.0.0.1:7893/log", timeout=1, headers={'Content-Type': 'application/json'},
                          data=json.dumps(msg))
        except Exception as ex:
            print("boskelHandler error, you can ignore this. " + str(ex), flush=True)


logger = Logger(name="SCRAUSO").logger
loggerSubmitter = Logger(name="SCRAUSO-Submitter").logger
loggerReceiver = Logger(name="SCRAUSO-Receiver").logger
