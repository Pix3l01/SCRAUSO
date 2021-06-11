import receiver
import db
import tomli
import sys
import sender


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
    except IOError:
        print("Io error")
        exit(1)
    except tomli.TOMLDecodeError:
        print("Can't load config")
        exit(2)
    assert 'general' in config, 'Missing block \'general\' in config'
    assert 'sender' in config, 'Missing block \'sender\' in config'
    assert 'db' in config['general'], 'Parameter \'db\' missing in config block [general]'
    assert 'port' in config['general'], 'Parameter \'ip\' missing in config block [general]'
    assert 'port' in config['general'], 'Parameter \'port\' missing in config block [general]'
    assert 'link' in config['sender'], 'Parameter \'link\' missing in config block [sender]'
    assert 'token' in config['sender'], 'Parameter \'token\' missing in config block [sender]'
    assert 'ip' in config['sender'], 'Parameter \'ip\' missing in config block [sender]'
    assert 'port' in config['sender'], 'Parameter \'port\' missing in config block [sender]'
    assert 'sender' in config['sender'], 'Parameter \'sender\' missing in config block [sender]'
    print('done!')
    return config


if __name__ == '__main__':
    class_dict = {'forcADsender': sender.forcADsender, 'ncsender': sender.ncsender, 'faustSender': sender.faustSender}
    if len(sys.argv) != 2:
        print('\nIt needs a config file as argument')
        exit(0)
    print('Loading configs', end=' ')
    config_dict = load_config(sys.argv[1])
    if config_dict['sender']['sender'] == 'forcADsender':
        sender_object = class_dict[config_dict['sender']['sender']](config_dict['general']['db'],
                                                                    config_dict['sender']['token'],
                                                                    config_dict['sender']['link'])
    elif config_dict['sender']['sender'] == 'ncsender':
        sender_object = class_dict[config_dict['sender']['sender']](config_dict['general']['db'],
                                                                    config_dict['sender']['token'],
                                                                    config_dict['sender']['ip'],
                                                                    config_dict['sender']['port'])
    elif config_dict['sender']['sender'] == 'faustSender':
        sender_object = class_dict[config_dict['sender']['sender']](config_dict['general']['db'],
                                                                    config_dict['sender']['ip'],
                                                                    config_dict['sender']['port'])
    else:
        print('Sender method not defined')
        exit(3)
    dbm = db.database(config_dict['general']['db'])
    print('Initializing database', end=' ')
    dbm.init_database()
    print('done!')
    print('Starting receiver')
    start_receiver(dbm, sender_object, config_dict['general']['ip'], config_dict['general']['port'])
