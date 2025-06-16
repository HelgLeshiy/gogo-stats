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

@app.route('/v1/players/add', methods=['POST'])
def flask_players_add():
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

@app.route('/v1/players/dmg_add', methods=['POST'])
def flask_players_dmg_add():
    logger.info("flask request", extra={"tags": {"url": request.url}})
    req = request.get_json()
    print(req)

    id = req["id"]
    dmg = req["dmg"]

    now = datetime.datetime.now(datetime.timezone.utc)

    conn = psycopg2.connect(dbname='kakebo', user='whisper', password='2whisper2', host='91.105.196.201', port="5000")
    rowcount = 0
    with conn.cursor() as curs:
        curs.execute('UPDATE gogo_stats SET dragon_dmg = %s WHERE id = %s AND date = (SELECT MAX(date) from gogo_stats WHERE id = %s)', (dmg, id, id,))
        rowcount = curs.rowcount
    conn.commit()
    conn.close()

    return str(rowcount), 200

@app.route('/v1/players', methods=['GET'])
def flask_players():
    logger.info("flask request", extra={"tags": {"url": request.url}})

    conn = psycopg2.connect(dbname='kakebo', user='whisper', password='2whisper2', host='91.105.196.201', port="5000")
    players = []
    with conn.cursor() as curs:
        curs.execute('''
                    select t.id, t.nickname, t.lvl, t.class, t.stage, t.power, t.dragon_dmg, t.date
                    from gogo_stats t
                    inner join (
                        select id, max(date) as MaxDate
                        from gogo_stats
                        group by id
                    ) tm on t.id = tm.id and t.date = tm.MaxDate
                    order by t.power desc
                    ''')
        rows = curs.fetchall()
        for row in rows:
            players.append({
                "id": row[0],
                "nickname": row[1],
                "lvl": row[2],
                "cls": row[3],
                "stage": row[4],
                "power": row[5],
                "dragon_dmg": 0 if row[6] is None else row[6],
                "update_date": row[7]
            })

    conn.close()

    return { "players": players }


#app.run('0.0.0.0', port=8001, debug=True)