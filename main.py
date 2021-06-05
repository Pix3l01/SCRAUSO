import receiver
import db


def start_receiver(dbm: db.database):
    receiver.setDbm(dbm)
    receiver.app.run()

if __name__ == '__main__':
    dbm = db.database('test.db')
    dbm.init_database()
    start_receiver(dbm)
