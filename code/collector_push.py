from dotenv import load_dotenv
import pyads
import psycopg2
import threading
import queue
from datetime import datetime, timezone
import os

load_dotenv()

AMS_NET_ID = os.getenv('AMS_NET_ID')
AMS_PORT   = int(os.getenv('AMS_PORT'))
DB_CONN    = (
    f"host={os.getenv('DB_HOST')} "
    f"port={os.getenv('DB_PORT')} "
    f"dbname={os.getenv('DB_NAME')} "
    f"user={os.getenv('DB_USER')} "
    f"password={os.getenv('DB_PASSWORD')}"
)
BATCH_SIZE = 20

plc  = pyads.Connection(AMS_NET_ID, AMS_PORT)
conn = psycopg2.connect(DB_CONN)
cur  = conn.cursor()

plc.open()
print("Connected to PLC and DB")

latest    = {'rTemperatureReadable1': None, 'rTemperatureReadable2': None, 'rPressureReadable1': None, 'rPressureReadable2': None, 'rPositionReadable': None, 'rForceReadable': None}
latest_ts = {'rTemperatureReadable1': None, 'rTemperatureReadable2': None, 'rPressureReadable1': None, 'rPressureReadable2': None, 'rPositionReadable': None, 'rForceReadable': None}
batch     = []
lock      = threading.Lock()
db_queue  = queue.Queue()
running   = True

def db_worker():
    while True:
        rows = db_queue.get()
        if rows is None:
            break
        cur.executemany(
            "INSERT INTO measurements (time, temperature_1, temperature_2, pressure_1, pressure_2, position, force) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            rows
        )
        conn.commit()
        p, pos, t = rows[-1][1], rows[-1][2], rows[-1][3]
        print(f"Inserted {len(rows)} rows — p={p:.2f} pos={pos:.2f} t={t:.2f}")

worker = threading.Thread(target=db_worker, daemon=True)
worker.start()

def flush_if_ready():
    if any(v is None for v in latest.values()):
        return
    # Brug gennemsnittet af de tre timestamps
    ts = min(latest_ts.values())
    batch.append((ts, latest['rTemperatureReadable1'], latest['rTemperatureReadable2'], latest['rPressureReadable1'], latest['rPressureReadable2'], latest['rPositionReadable'], latest['rForceReadable']))
    latest['rTemperatureReadable1']    = None
    latest['rTemperatureReadable2']    = None
    latest['rPressureReadable1']       = None
    latest['rPressureReadable2']       = None
    latest['rPositionReadable']        = None
    latest['rForceReadable']           = None

    if len(batch) >= BATCH_SIZE:
        db_queue.put(batch.copy())
        batch.clear()

@plc.notification(pyads.PLCTYPE_REAL)
def on_temperture1(handle, name, timestamp, value):
    with lock:
        latest['rTemperatureReadable1']    = value
        latest_ts['rTemperatureReadable1'] = datetime.now(timezone.utc)
        flush_if_ready()

@plc.notification(pyads.PLCTYPE_REAL)
def on_temperture2(handle, name, timestamp, value):
    with lock:
        latest['rTemperatureReadable2']    = value
        latest_ts['rTemperatureReadable2'] = datetime.now(timezone.utc)
        flush_if_ready()
    
@plc.notification(pyads.PLCTYPE_REAL)
def on_pressure1(handle, name, timestamp, value):
    with lock:
        latest['rPressureReadable1']    = value
        latest_ts['rPressureReadable1'] = datetime.now(timezone.utc)
        flush_if_ready()

@plc.notification(pyads.PLCTYPE_REAL)
def on_pressure2(handle, name, timestamp, value):
    with lock:
        latest['rPressureReadable2']    = value
        latest_ts['rPressureReadable2'] = datetime.now(timezone.utc)
        flush_if_ready()

@plc.notification(pyads.PLCTYPE_REAL)
def on_position(handle, name, timestamp, value):
    with lock:
        latest['rPositionReadable']    = value
        latest_ts['rPositionReadable'] = datetime.now(timezone.utc)
        flush_if_ready()

@plc.notification(pyads.PLCTYPE_REAL)
def on_force(handle, name, timestamp, value):
    with lock:
        latest['rForceReadable']    = value
        latest_ts['rForceReadable'] = datetime.now(timezone.utc)
        flush_if_ready()

attr = pyads.NotificationAttrib(
    length=4,
    trans_mode=pyads.constants.ADSTRANS_SERVERCYCLE,
    max_delay=0.0,
    cycle_time=0.01
)

h1 = plc.add_device_notification('MAIN.rTemperatureReadable1',    attr, on_temperture1)
h2 = plc.add_device_notification('MAIN.rTemperatureReadable2',    attr, on_temperture2)
h3 = plc.add_device_notification('MAIN.rPressureReadable1', attr, on_pressure1)
h4 = plc.add_device_notification('MAIN.rPressureReadable2',    attr, on_pressure2)
h5 = plc.add_device_notification('MAIN.rPositionReadable',    attr, on_position)
h6 = plc.add_device_notification('MAIN.rForceReadable', attr, on_force)

print("Listening — tryk Enter for at stoppe")
input()  # Enter stopper scriptet 

print("Stopped")
with lock:
    if batch:
        db_queue.put(batch.copy())
db_queue.put(None)
worker.join()

plc.del_device_notification(*h1)
plc.del_device_notification(*h2)
plc.del_device_notification(*h3)
plc.del_device_notification(*h4)
plc.del_device_notification(*h5)
plc.del_device_notification(*h6)
plc.close()
cur.close()
conn.close()
print("Afsluttet")