
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

WATCH_DOG_INTERVAL = 100

AOF_FILE = os.path.join(BASE_DIR, 'dump.aof')
RDB_FILE = os.path.join(BASE_DIR, 'dump.rdb')


