from flask import Flask
from flask import request
from flask import jsonify

import os

import psycopg2
from psycopg2.extras import NamedTupleCursor

import logging
import datetime

logger = logging.getLogger("pylogger")

logger.setLevel(logging.DEBUG)

logger.info("starting server...")

app = Flask("magav2")

@app.route('/v1/player', methods=['POST'])
def flask_player():
    logger.info("flask request", extra={"tags": {"url": request.url}})
    req = request.get_json()
    print(req)

    nickname = req["nickname"]
    id = req["id"]
    lvl = req["lvl"]
    cls = req["class"]
    stage = req["stage"]
    power = req["power"]

    now = datetime.datetime.now(datetime.timezone.utc)

    conn = psycopg2.connect(dbname='kakebo', user='whisper', password='2whisper2', host='91.105.196.201', port="5000")

    with conn.cursor() as curs:
        curs.execute('INSERT INTO gogo_stats (id, nickname, lvl, class, stage, power, date) VALUES (%s, %s, %s, %s, %s, %s, %s)', (id, nickname, lvl, cls, stage, power, now,))
    conn.commit()
    conn.close()

    return "", 200


#app.run('0.0.0.0', port=8001, debug=True)