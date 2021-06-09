import requests
from requests.structures import CaseInsensitiveDict
import random
import string
import time
import json
import sys


def send_flags(exploit: str = 'banana'):
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["Content-Type"] = "application/json"
    flags = []
    while True:
        f = open('flagDump.txt', 'a')
        for _ in range(100):
            letters = string.digits + string.ascii_letters
            result_str = 'flag{'
            result_str += ''.join(random.choice(letters) for i in range(20))
            result_str += '}'
            flags.append(result_str)
        data = {'exploit': exploit, 'flags': flags}
        for flag in flags:
            f.write(flag + '\n')
        f.close()
        r = requests.post("http://127.0.0.1:5000/", data=json.dumps(data), headers=headers)
        print(str(r.status_code) + '\n' + r.text)
        time.sleep(10)
        flags = flags[2:4]


if __name__ == '__main__':
    send_flags(sys.argv[1])
