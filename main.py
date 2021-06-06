import receiver
import db
import tomli
import sys


def start_receiver(dbm: db.database):
    receiver.setDbm(dbm)
    receiver.app.run()


def load_config(path: str):
    try:
        with open(sys.argv[1], encoding="utf-8") as f:
            config_dict = tomli.load(f)
    except IOError:
        print("Io error")
        exit(1)
    except tomli.TOMLDecodeError:
        print("Can't load config")
        exit(2)
    assert 'link' in config_dict, 'Parameter \'link\' missing in config'
    assert 'db' in config_dict, 'Parameter \'db\' missing in config'
    assert 'token' in config_dict, 'Parameter \'token\' missing in config'
    print('done!')
    return config_dict


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('\nIt needs a config file as argument')
        exit(0)
    print('Loading configs', end=' ')
    config_dict = load_config(sys.argv[0])
    dbm = db.database('test.db')
    print('Initializing database', end=' ')
    dbm.init_database()
    print('done!')
    print('Starting receiver')
    start_receiver(dbm)
