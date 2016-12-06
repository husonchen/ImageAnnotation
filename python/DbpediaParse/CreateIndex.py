import sqlite3 as lite

con = lite.connect('WikiGraph.db')
cur = con.cursor()

cur.execute('PRAGMA journal_mode=WAL')
cur.execute('PRAGMA temp_store=2')
cur.execute('CREATE INDEX idx_mentions_out ON mentions(out_page_id)')