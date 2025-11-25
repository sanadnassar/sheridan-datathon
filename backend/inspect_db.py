import sqlite3
import os

db_path = 'data/buildings.db'
if not os.path.exists(db_path):
    db_path = os.path.join(os.path.dirname(__file__), '..', db_path)

print('Using DB:', db_path)
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# Show table info
try:
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    print('Tables:', cur.fetchall())

    cur.execute('PRAGMA table_info(rooftops)')
    print('rooftops columns:', cur.fetchall())

    cur.execute('SELECT COUNT(*) FROM rooftops')
    count = cur.fetchone()[0]
    print('rooftops count:', count)

    cur.execute('SELECT easting, northing, area FROM rooftops LIMIT 10')
    rows = cur.fetchall()
    print('Sample rows (easting, northing, area):')
    for r in rows:
        print(' ', r)

    cur.execute('SELECT MIN(easting), MAX(easting), MIN(northing), MAX(northing) FROM rooftops')
    mins = cur.fetchone()
    print('Easting/ Northing min/max:', mins)

    cur.execute('SELECT COUNT(DISTINCT area) FROM rooftops')
    print('Distinct area count:', cur.fetchone()[0])

    cur.execute('SELECT area, COUNT(*) FROM rooftops GROUP BY area ORDER BY COUNT(*) DESC LIMIT 10')
    print('Top 10 area frequencies:')
    for r in cur.fetchall():
        print(' ', r)
finally:
    conn.close()
