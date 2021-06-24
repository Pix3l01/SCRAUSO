import receiver
import db
import tomli
import sys
import sender
from time import sleep
from threading import Thread


def start_receiver(dbm: db.database, sender_type, ip: str, port: int):
    receiver.setDbm(dbm)
    receiver.setSender(sender_type)
    receiver.app.run(host=ip, port=port)


def load_config(path: str):
    print('I\'m lazy so the program check for the existence of every parameter of the config even if not necessary. \
So if you have error add also useless dummy parameters')
    try:
        with open(path, encoding="utf-8") as f:
            config = tomli.load(f)
    except IOError as e:
        print(f"Io error: {e}")
        exit(1)
    except tomli.TOMLDecodeError:
        print("Can't load config")
        exit(2)
    assert 'general' in config, 'Missing block \'general\' in config'
    assert 'sender' in config, 'Missing block \'sender\' in config'
    assert 'port' in config['general'], 'Parameter \'ip\' missing in config block [general]'
    assert 'port' in config['general'], 'Parameter \'port\' missing in config block [general]'
    assert 'scheduled_check' in config['general'], 'Parameter \'scheduled_check\' missing in config block [general]'
    assert 'address' in config['database'], 'Parameter \'address\' missing in config block [database]'
    assert 'name' in config['database'], 'Parameter \'name\' missing in config block [database]'
    assert 'username' in config['database'], 'Parameter \'username\' missing in config block [database]'
    assert 'password' in config['database'], 'Parameter \'password\' missing in config block [database]'
    assert 'link' in config['sender'], 'Parameter \'link\' missing in config block [sender]'
    assert 'token' in config['sender'], 'Parameter \'token\' missing in config block [sender]'
    assert 'ip' in config['sender'], 'Parameter \'ip\' missing in config block [sender]'
    assert 'port' in config['sender'], 'Parameter \'port\' missing in config block [sender]'
    assert 'sender' in config['sender'], 'Parameter \'sender\' missing in config block [sender]'
    print('done!')
    return config


def flags_per_exploit(database):
    query = "SELECT DISTINCT exploit FROM submitter"
    exploits = database.exec_query(query)
    print(exploits)
    for exploit in exploits:
        qCount = f"SELECT COUNT(flag) FROM submitter WHERE exploit = '{exploit[0]}' AND status = 1 OR status = 5"
        print(f"Query: {qCount}")
        i = database.exec_query(qCount)
        print(f'Flags correctly submitted for {exploit[0]}: {i[0][0]}')
    return


def repeated_check(sleep_time: float, send: sender, database: db):
    while True:
        print("Checking for leftover flag")
        query = "SELECT flag FROM submitter WHERE status=0"
        missed_flags = []
        try:
            missed_flags = database.exec_query(query)
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
    class_dict = {'forcADsender': sender.forcADsender, 'ncsender': sender.ncsender, 'faustSender': sender.faustSender}
    if len(sys.argv) != 2:
        print('\nIt needs a config file as argument')
        exit(0)
    print('Loading configs', end=' ')
    config_dict = load_config(sys.argv[1])
    dbm = db.database(config_dict['database']['address'], config_dict['database']['name'], config_dict['database']['username'], config_dict['database']['password'])
    print('Initializing database', end=' ')
    dbm.init_database()
    print('done!')
    if config_dict['sender']['sender'] == 'forcADsender':
        sender_object = class_dict[config_dict['sender']['sender']](dbm,
                                                                    config_dict['sender']['token'],
                                                                    config_dict['sender']['link'])
    elif config_dict['sender']['sender'] == 'ncsender':
        sender_object = class_dict[config_dict['sender']['sender']](dbm,
                                                                    config_dict['sender']['token'],
                                                                    config_dict['sender']['ip'],
                                                                    config_dict['sender']['port'])
    elif config_dict['sender']['sender'] == 'faustSender':
        sender_object = class_dict[config_dict['sender']['sender']](dbm,
                                                                    config_dict['sender']['ip'],
                                                                    config_dict['sender']['port'])
    else:
        print('Sender method not defined')
        exit(3)
    print('Starting missed flag checker')
    thread = Thread(target=repeated_check, args=(config_dict['general']['scheduled_check'], sender_object, dbm))
    thread.start()
    print('Starting receiver')
    start_receiver(dbm, sender_object, config_dict['general']['ip'], config_dict['general']['port'])
