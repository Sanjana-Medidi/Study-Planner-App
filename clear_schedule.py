import sqlite3

# Connect to your database
conn = sqlite3.connect('studyplanner.db')
c = conn.cursor()

# Delete all records from the schedule table
c.execute('DELETE FROM schedule')
conn.commit()
conn.close()

print("✅ All schedule entries deleted.")
