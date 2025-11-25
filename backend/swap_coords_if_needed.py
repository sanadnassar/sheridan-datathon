import sqlite3
import os
import shutil
import time

DB_PATH = 'data/buildings.db'
if not os.path.exists(DB_PATH):
    DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'buildings.db')

print('Using DB:', DB_PATH)
if not os.path.exists(DB_PATH):
    raise SystemExit('Database not found')

# Inspect medians / ranges to detect swapped columns
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

try:
    cur.execute('SELECT COUNT(*) FROM rooftops')
    total = cur.fetchone()[0]
    print('Rows in rooftops:', total)

    # Get approximate medians by sampling a few percent (avoid full scan)
    cur.execute('SELECT easting, northing FROM rooftops LIMIT 1000')
    sample = cur.fetchall()
    if not sample:
        raise SystemExit('No rooftops rows')

    eastings = [r[0] for r in sample]
    northings = [r[1] for r in sample]
    median_easting = sorted(eastings)[len(eastings)//2]
    median_northing = sorted(northings)[len(northings)//2]

    print('Sample median easting:', median_easting)
    print('Sample median northing:', median_northing)

    # Heuristic: in OSGB36 for London, typical easting ~300k-600k, northing ~100k-300k
    # If median_easting < 300000 and median_northing > 300000 -> likely swapped
    swapped = False
    if median_easting < 300000 and median_northing > 300000:
        swapped = True

    if not swapped:
        print('No swap detected. No action required.')
        raise SystemExit(0)

    print('Swap detected! Preparing to swap easting/northing in DB.')

    # Backup DB
    t = time.strftime('%Y%m%d-%H%M%S')
    backup_path = DB_PATH + f'.bak.{t}'
    shutil.copy2(DB_PATH, backup_path)
    print(f'Backup created at {backup_path}')

    # Perform safe swap by creating new table and moving data
    cur.execute('PRAGMA foreign_keys = OFF')
    conn.commit()

    cur.execute('ALTER TABLE rooftops RENAME TO rooftops_old')
    conn.commit()

    # Create new rooftops table with same schema (easting, northing, area)
    cur.execute('CREATE TABLE rooftops (easting REAL, northing REAL, area REAL)')
    conn.commit()

    # Insert swapped data: treat old northing as easting and old easting as northing
    cur.execute('INSERT INTO rooftops (easting, northing, area) SELECT northing, easting, area FROM rooftops_old')
    conn.commit()

    # Drop old table
    cur.execute('DROP TABLE rooftops_old')
    conn.commit()

    print('Swap completed successfully.')

finally:
    conn.close()
