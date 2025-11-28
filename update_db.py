import sqlite3

conn = sqlite3.connect('study_schedule.db')  # Make sure this matches the DB used in app.py
c = conn.cursor()

# Rename old table
c.execute("ALTER TABLE schedule RENAME TO old_schedule")

# Create new schedule table with required columns
c.execute('''
    CREATE TABLE schedule (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT NOT NULL,
        daily_time INTEGER NOT NULL,
        date TEXT NOT NULL,
        completed INTEGER DEFAULT 0
    )
''')

# Optional: Copy existing data from old_schedule to new schedule table (filling date with today)
from datetime import datetime
today = datetime.today().strftime('%Y-%m-%d')
c.execute("INSERT INTO schedule (subject, daily_time, date, completed) SELECT subject, daily_time, ?, 0 FROM old_schedule", (today,))

# Drop the old table
c.execute("DROP TABLE old_schedule")

conn.commit()
conn.close()

print("✅ Database schema updated successfully!")
