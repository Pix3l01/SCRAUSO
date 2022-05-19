import receiver
import db
import tomli
import sys
import sender
from time import sleep
from threading import Thread


def start_receiver(dbm: db.database, sender_type, server_ip: str, server_port: int):
    receiver.setDbm(dbm)
    receiver.setSender(sender_type)
    receiver.app.run(host=server_ip, port=server_port)


def load_config(path: str):
    try:
        with open(path, encoding="utf-8") as f:
            config = tomli.load(f)
    except IOError as e:
        print(f"Io error: {e}")
        exit(1)
    except tomli.TOMLDecodeError:
        print("Can't load config, maybe a parameter isn't specified")
        exit(2)
    if 'general' not in config:
        print('Missing block \'general\' in config')
        exit(3)
    if 'sender' not in config:
        print('Missing block \'sender\' in config')
        exit(3)
    if 'db' not in config['general']:
        print('Parameter \'db\' missing in config block [general]')
        exit(3)
    if 'sender' not in config['sender']:
        print('Parameter \'sender\' missing in config block [sender]')
        exit(3)
    print('done!')
    return config['general'], config['sender']


def flags_per_exploit(database):
    query = "SELECT DISTINCT exploit FROM submitter"
    exploits = database.exec_query(query, ())
    print(exploits)
    for exploit in exploits:
        qCount = f"SELECT COUNT(flag) FROM submitter WHERE exploit = '{exploit[0]}' AND status = 1"
        i = database.exec_query(qCount, ())
        print(f'Flags correctly submitted for {exploit[0]}: {i[0][0]}')
    return


def repeated_check(sleep_time: float, send: sender, database: db):
    while True:
        print("Checking for leftover flag")
        query = "SELECT flag FROM submitter WHERE status=0 OR status=5"
        missed_flags = []
        try:
            missed_flags = database.exec_query(query, ())
        except Exception as e:
            print('S\'è sminichiato tutto leggendo')
            print(e)
        if len(missed_flags) > 0:
            print(f'{len(missed_flags)} missed flag(s) found')
            send.send()
        else:
            print('No missed flags found')
        flags_per_exploit(database)
        print(f'Sleeping for {sleep_time} seconds')
        sleep(sleep_time)


if __name__ == '__main__':
    class_dict = {'forcADsender': sender.forcADsender, 'ncsender': sender.ncsender, 'faustSender': sender.faustSender,
                  'ctfzone': sender.ctfzone, 'saarSender': sender.saarSender}
    if len(sys.argv) != 2:
        print('\nIt needs a config file as argument')
        exit(0)
    print('Loading config')
    general_config, sender_config = load_config(sys.argv[1])
    db_path = general_config['db']
    sender_method = sender_config['sender']

    if sender_method == 'forcADsender':
        if 'token' not in sender_config:
            print('Missing token in config')
            exit(3)
        token = sender_config['token']
        if 'host' not in sender_config:
            print('Missing submission host in config')
            exit(0)
        host = sender_config['host']
        sender_object = class_dict[sender_method](db_path, token, host)

    elif sender_method == 'ncsender':
        if 'token' not in sender_config:
            print('Missing token in config')
            exit(3)
        token = sender_config['token']
        if 'host' not in sender_config:
            print('Missing submission host in config')
            exit(0)
        host = sender_config['host']
        if 'port' not in sender_config:
            print('Missing submission server port in config')
            exit(3)
        port = sender_config['port']
        sender_object = class_dict[sender_method](db_path, token, host, port)

    elif sender_method == 'faustSender':
        if 'host' not in sender_config:
            print('Missing submission host in config')
            exit(0)
        host = sender_config['host']
        if 'port' not in sender_config:
            print('Missing submission server port in config')
            exit(3)
        port = sender_config['port']
        sender_object = class_dict[sender_method](db_path, host, port)

    elif sender_method == 'ctfzone':
        if 'token' not in sender_config:
            print('Missing token in config')
            exit(3)
        token = sender_config['token']
        if 'host' not in sender_config:
            print('Missing submission host in config')
            exit(0)
        host = sender_config['host']
        sender_object = class_dict[sender_method](db_path, token, host)

    elif sender_method == 'saarSender':
        if 'host' not in sender_config:
            print('Missing submission host in config')
            exit(0)
        host = sender_config['host']
        if 'port' not in sender_config:
            print('Missing submission server port in config')
            exit(3)
        port = sender_config['port']
        sender_object = class_dict[sender_method](db_path, host, port)
    else:
        print('Sender method not defined')
        exit(3)

    dbm = db.database(db_path)
    print('Initializing database', end=' ')
    dbm.init_database()
    print('done!')

    print('Starting missed flag checker')
    delay = 30
    if 'scheduled_check' not in general_config:
        print(f'No delay for scheduled check specified in config. Using default {delay}')
    else:
        delay = general_config['scheduled_check']
    thread = Thread(target=repeated_check, args=(delay, sender_object, dbm))
    thread.start()

    print('Starting receiver')
    ip = '0.0.0.0'
    receiver_port = 5000
    if 'ip' not in general_config or general_config['ip'] == '':
        print(f'No server ip specified in config. Using default {ip}')
    else:
        ip = general_config['ip']

    if 'port' not in general_config or general_config['port'] == '':
        print(f'No server port specified in config. Using default {receiver_port}')
    else:
        receiver_port = general_config['port']
    start_receiver(dbm, sender_object, ip, receiver_port)
