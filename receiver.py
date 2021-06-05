from flask import Flask, request
import db

dbm: db.database
tick = 0
app = Flask(__name__)


def setDbm(dbman: db.database):
    global dbm
    dbm = dbman


@app.route('/', methods=['GET', 'POST'])
def index():
    msg = ''
    if request.method == 'POST':
        content = request.json
        exploit = content['exploit']
        flags = content['flags']
        msg = "The exploit " + exploit + " has " + str(len(flags)) + " flags!"
        for flag in flags:
            # TODO implement prepared statement
            query = f"INSERT INTO Submitter VALUES ('{flag}', 0, 0, '{exploit}')"
            dbm.exec_query(query)

    else:
        msg = '''POST / HTTP/1.1
                Host: 127.0.0.1:5000
                Accept: application/json
                Content-Type: application/json
                
                {
                  "exploit": "invented exploit name",
                  "flags": [
                    "array with plain text flags"
                  ]
                }'''
    return msg
