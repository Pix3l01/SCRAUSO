from flask import Flask, request
import db
import sqlite3

dbm: db.database
tick = 0
app = Flask(__name__)


def setDbm(dbman: db.database):
    global dbm
    dbm = dbman


@app.route('/tick')
def updateTick():
    global tick
    t = request.args.get('t', type=int)
    if t:
        tick = request.args.get('t')
        return f"Tick set to {tick}"
    else:
        return "Must contain parameter integer 't'"


@app.route('/', methods=['GET', 'POST'])
def index():
    global tick
    msg = ''
    if request.method == 'POST':
        duplicate = 0
        content = request.json
        exploit = content['exploit']
        flags = content['flags']
        msg = "The exploit " + exploit + " has " + str(len(flags)) + " flags!"
        for flag in flags:
            # TODO implement prepared statement
            query = f"INSERT INTO Submitter VALUES ('{flag}', {tick}, 0, '{exploit}', 0)"
            try:
                dbm.exec_query(query)
            except sqlite3.IntegrityError:
                duplicate += 1
        msg += f"<br>Duplicate flags: {duplicate}"
        if duplicate < len(flags):
            print("New flags!")
            # TODO notice sender.py that there are new flags

    else:
        msg = '''POST / HTTP/1.1<br>
                Host: 127.0.0.1:5000<br>
                Accept: application/json<br>
                Content-Type: application/json<br>
                {<br>
                  "exploit": "invented exploit name",<br>
                  "flags": [<br>
                    "array with plain text flags"<br>
                  ]<br>
                }'''
    return msg
