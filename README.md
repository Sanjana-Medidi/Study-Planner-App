# Study-Planner-App
# 📚 Personal Study Planner

A web-based application designed to help students organize their study routines and manage time effectively. This project demonstrates full-stack logic using Python, Flask, and SQLite.


## 🚀 Overview
This application solves the problem of disorganized study schedules. It allows users to input their subjects, deadlines, and available study hours per day. The application then runs an algorithm to automatically distribute the workload and generate a clear, day-by-day study table.

## ✨ Key Features
* **Smart Scheduling Algorithm:** Automatically calculates and distributes study hours across days based on the deadline provided.
* **Progress Tracking:** Users can view their generated schedule and mark specific study sessions as "Completed."
* **Data Persistence:** Uses **SQLite** to store schedules and subject details, ensuring data is saved even after the browser is closed.
* **Dynamic Inputs:** Supports adding multiple subjects and adjusting daily study limits.
* **Clean UI:** A user-friendly interface built with HTML/CSS and Jinja2 templates.

## 🛠️ Tech Stack
* **Language:** Python 3.x
* **Framework:** Flask (Web Server)
* **Database:** SQLite
* **Frontend:** HTML, CSS, JavaScript (Basic DOM manipulation)
* **Logic:** Custom Python Algorithm for Date & Time Calculation

## 📂 Project Structure
* `app.py` - The main entry point of the application (Routing & Logic).
* `init_db.py` / `setup_db.py` - Scripts to initialize and structure the database.
* `templates/` - HTML files for the user interface.
* `static/` - CSS styling files.
* `visualize.py` - *Logic included for future data analysis features.*

## ⚙️ How to Run Locally

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/Study-Planner-App.git](https://github.com/YOUR_USERNAME/Study-Planner-App.git)
    cd Study-Planner-App
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Initialize Database**
    ```bash
    python init_db.py
    ```

4.  **Run the App**
    ```bash
    python app.py
    ```

5.  **View in Browser**
    Open your web browser and go to `http://127.0.0.1:5000/`

## 🔮 Future Scope
* **AI Integration:** Planning to implement a Machine Learning algorithm to suggest optimal study times based on user completion history.
* **Visual Analytics:** Implementing graphical charts to visualize study trends.
* **User Authentication:** Adding login/signup functionality for personalized accounts.

https://github.com/user-attachments/assets/69661358-ff94-4bd2-a085-95625be25c8b




