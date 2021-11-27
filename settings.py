
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

WATCH_DOG_CYCLE = 100

AOF_FILE = os.path.join(BASE_DIR, 'dump.aof')
RDB_FILE = os.path.join(BASE_DIR, 'dump.rdb')

SENTINEL_MASTER_ADDR = ('127.0.0.1', 9527)


