import sqlite3
import matplotlib.pyplot as plt

# Connect to the correct database file
conn = sqlite3.connect('study_schedule.db')
cursor = conn.cursor()

# Just to confirm the structure
cursor.execute("PRAGMA table_info(schedule)")
columns = cursor.fetchall()
print("📋 Table columns:", [col[1] for col in columns])

# Fetch data grouped by subject
cursor.execute("SELECT subject, SUM(daily_time) FROM schedule GROUP BY subject")
data = cursor.fetchall()

# Close the connection
conn.close()

# Separate data for plotting
subjects = [row[0] for row in data]
hours = [row[1] for row in data]

# Plotting
plt.figure(figsize=(8, 5))
plt.bar(subjects, hours, color='skyblue')
plt.title("Total Study Time per Subject")
plt.xlabel("Subjects")
plt.ylabel("Total Hours")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
