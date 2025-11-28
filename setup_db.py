import sqlite3

conn = sqlite3.connect('study_planner.db')
c = conn.cursor()

# Drop table if it already exists (clean reset)
c.execute('DROP TABLE IF EXISTS schedule')

# Recreate schedule table with correct columns
c.execute('''
    CREATE TABLE IF NOT EXISTS schedule (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_name TEXT NOT NULL,
        study_date DATE NOT NULL,
        hours INTEGER NOT NULL,
        minutes INTEGER NOT NULL,
        completed INTEGER DEFAULT 0
    )
''')

conn.commit()
conn.close()
