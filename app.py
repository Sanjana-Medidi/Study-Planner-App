from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime, timedelta
from collections import defaultdict

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('studyplanner.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS schedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject_name TEXT NOT NULL,
            hours INTEGER,
            minutes INTEGER,
            study_date TEXT NOT NULL,
            completed INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    subjects = request.form.getlist('subject')
    deadlines = request.form.getlist('deadline')
    daily_hours = float(request.form.get('daily_hours'))

    if not subjects or not deadlines or daily_hours <= 0:
        return redirect(url_for('index'))

    today = datetime.now().date()
    daily_minutes = int(daily_hours * 60)

    # Step 1: Prepare subject info with days left
    subjects_info = []
    max_deadline = today
    for i in range(len(subjects)):
        subject = subjects[i]
        deadline = datetime.strptime(deadlines[i], "%Y-%m-%d").date()
        if deadline > max_deadline:
            max_deadline = deadline
        days_left = (deadline - today).days + 1
        if days_left > 0:
            subjects_info.append({
                'name': subject,
                'deadline': deadline,
                'days_left': days_left
            })

    # Generate weighted schedule
    schedules = []
    for day_offset in range((max_deadline - today).days + 1):
        current_date = today + timedelta(days=day_offset)

        # Filter subjects still pending
        available_subjects = [s for s in subjects_info if s['deadline'] >= current_date]

        # Total weight: inverse of days_left (closer deadlines = higher weight)
        total_weight = sum(1 / s['days_left'] for s in available_subjects)

        for s in available_subjects:
            weight = (1 / s['days_left']) / total_weight
            subject_minutes = int(weight * daily_minutes)
            h = subject_minutes // 60
            m = subject_minutes % 60
            schedules.append((s['name'], h, m, current_date.strftime("%Y-%m-%d")))

    #  DB save
    conn = sqlite3.connect('studyplanner.db')
    c = conn.cursor()
    for entry in schedules:
        c.execute('''
            INSERT INTO schedule (subject_name, hours, minutes, study_date, completed)
            VALUES (?, ?, ?, ?, 0)
        ''', entry)
    conn.commit()
    conn.close()

    return redirect(url_for('view_schedule'))

@app.route('/view_schedule')
def view_schedule():
    today = datetime.now().date()
    conn = sqlite3.connect('studyplanner.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # Identify and remove missed sessions
    c.execute('''
        SELECT id, subject_name, hours, minutes, study_date
        FROM schedule
        WHERE completed = 0
    ''')
    tasks = c.fetchall()

    missed_time = defaultdict(int)
    for row in tasks:
        task_date = datetime.strptime(row['study_date'], "%Y-%m-%d").date()
        if task_date < today:
            c.execute("DELETE FROM schedule WHERE id = ?", (row['id'],))
            total_minutes = row['hours'] * 60 + row['minutes']
            missed_time[row['subject_name']] += total_minutes

    # Redistribute missed time
    for subject, total_minutes in missed_time.items():
        c.execute('''
            SELECT MAX(study_date) FROM schedule
            WHERE subject_name = ? AND completed = 0
        ''', (subject,))
        result = c.fetchone()
        if result and result[0]:
            deadline = datetime.strptime(result[0], "%Y-%m-%d").date()
            days_left = (deadline - today).days + 1
            if days_left <= 0:
                continue

            per_day = total_minutes // days_left
            remaining = total_minutes % days_left

            for i in range(days_left):
                date = today + timedelta(days=i)
                minutes = per_day + (1 if i < remaining else 0)
                h = minutes // 60
                m = minutes % 60

                # Update existing or insert new
                c.execute('''
                    SELECT id, hours, minutes FROM schedule
                    WHERE subject_name = ? AND study_date = ? AND completed = 0
                ''', (subject, date.strftime("%Y-%m-%d")))
                existing = c.fetchone()

                if existing:
                    total = (existing['hours'] * 60 + existing['minutes']) + minutes
                    c.execute('''
                        UPDATE schedule SET hours = ?, minutes = ?
                        WHERE id = ?
                    ''', (total // 60, total % 60, existing['id']))
                else:
                    c.execute('''
                        INSERT INTO schedule (subject_name, hours, minutes, study_date, completed)
                        VALUES (?, ?, ?, ?, 0)
                    ''', (subject, h, m, date.strftime("%Y-%m-%d")))

    conn.commit()

    # Step 3: Fetch and display updated schedule
    c.execute('''
        SELECT id, subject_name, hours, minutes, study_date, completed
        FROM schedule
        ORDER BY study_date
    ''')
    schedule = c.fetchall()
    conn.close()
    return render_template('schedule.html', schedule=schedule)

@app.route('/mark_completed/<int:schedule_id>', methods=['POST'])
def mark_completed(schedule_id):
    conn = sqlite3.connect('studyplanner.db')
    c = conn.cursor()
    c.execute('DELETE FROM schedule WHERE id = ?', (schedule_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('view_schedule'))

if __name__ == '__main__':
    app.run(debug=True)
