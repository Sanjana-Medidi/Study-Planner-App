import sqlite3

conn = sqlite3.connect('study_schedule.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS schedule (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT NOT NULL,
        daily_time INTEGER NOT NULL,
        date TEXT NOT NULL,
        completed INTEGER DEFAULT 0
    )
''')

conn.commit()
conn.close()

print("✅ Database and table created with 'date' and 'completed' columns.")
