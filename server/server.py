from flask import Flask, render_template, request
from flask_socketio import SocketIO
from random import random
from threading import Lock
from datetime import datetime
import os
import sqlite3
from flask import abort

DATABASE = 'game.sqlite'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, DATABASE)

thread = None
thread_lock = Lock()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'donsky!'
socketio = SocketIO(app, cors_allowed_origins='*', ping_timeout=10, ping_interval=5)

def get_current_datetime():
    now = datetime.now()
    return now.strftime("%m/%d/%Y %H:%M:%S")

def background_thread():
    print("Generating random sensor values")
    while True:
        dummy_sensor_value = round(random() * 100, 3)
        socketio.emit('updateSensorData', {'value': dummy_sensor_value, "date": get_current_datetime()})
        socketio.sleep(1)


def get_db_connection():
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def get_rows(query):
    conn = get_db_connection()
    cur = conn.cursor()
    cur = cur.execute(query)
    return [dict(row) for row in cur.fetchall()]

def get_single_row(query):
    conn = get_db_connection()
    cur = conn.cursor()
    cur = cur.execute(query)
    return dict(cur.fetchone())

def insert_to_db(query):
    print("--+"*10)
    print(query)
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur = cur.execute(query)
        conn.commit()
    except sqlite3.IntegrityError as e:
        print(e)
    finally:
        conn.close()
    
    
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/player/<id>')
def player(id=1):
    if id not in ['1', '2', '3', '4']:
        return abort(404)
    query = f"SELECT * FROM players WHERE ix={id}"
    player_info = get_single_row(query)
    return render_template('player.html', player=player_info)

@app.route('/submit_code', methods=['POST'])
def submit_code():
    data = request.json
    default_name = data.get('name', "player-" + data['player'])
    # try:
    insert_to_db(f"UPDATE 'players' SET name='{default_name}', code={data['code']} WHERE ix={data['player']}")
    # except Exception as exp:
    #     print(exp)
    return "ok"



@socketio.on('ENABLE_BUZZER')
def enable_buzzer():
    insert_to_db("UPDATE 'players' SET timestamp = NULL")
    socketio.emit("ENABLE_BUZZER")
    print("--------- Buzzer is ON ✅ ---------")

@socketio.on('DISABLE_BUZZER')
def disable_buzzer():
    socketio.emit("DISABLE_BUZZER")
    print("--------- Buzzer is OFF ❌ ---------")
    
@socketio.on('BUZZ_IN')
def buzz(msg):
    print(msg)
    insert_to_db(f"UPDATE 'players' SET timestamp={msg['timestamp']} WHERE code={msg['code']}")
    print("--------- 🔥 BUZZ 🔥 ---------")

@socketio.on('BUZZER_RESULTS')
def buzzer_results():
    players = get_rows("SELECT * FROM players")
    players = list(filter(lambda p: p['timestamp'] is not None, players))
    ordered_players = sorted(players, key=lambda row: row['timestamp'])
    socketio.emit("PLAYERS_ORDER", ordered_players)
    
@socketio.on('connect')
def connect():
    global thread
    print('Client connected')
    socketio.sleep(5)
    socketio.emit("START", {"name": "Marwan Rassi"})
    # global thread
    # with thread_lock:
    #     if thread is None:
    #         thread = socketio.start_background_task(background_thread)

"""
Decorator for disconnect
"""
@socketio.on('disconnect')
def disconnect():
    print('Client disconnected',  request.sid)

if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))