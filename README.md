# Time-Table-Generator
```markdown
# School Timetable Generator API 🏫📅

A fast, constraint-based timetable generator built with **Python**, **FastAPI**, and **Google OR-Tools**. 

This backend service takes a list of teachers, classrooms, classes, and lesson requirements, and mathematically calculates a 100% clash-free weekly schedule. It also includes an exporter to convert the raw JSON schedules into downloadable CSV files for Excel/Google Sheets.

## 🌟 Features

* **Constraint Programming Engine:** Uses Google OR-Tools to solve complex scheduling combinations.
* **Hard Constraints:** Guarantees no double-booking for teachers, rooms, or classes. Honors room capacity and lab requirements.
* **Soft Constraints:** Automatically minimizes teacher gap hours (idle periods) and prevents the same subject from being taught multiple times a day to the same class.
* **Interactive API Docs:** Built with FastAPI, providing an out-of-the-box Swagger UI to test the engine.
* **CSV Export:** Converts generated JSON schedules into formatted 2D grids (Days vs. Periods).

---

## 📂 Project Structure

school_timetable/
├── app/
│   ├── __init__.py
│   ├── models.py       # Pydantic data validation schemas
│   ├── solver.py       # Google OR-Tools constraint logic
│   ├── api.py          # FastAPI route definitions
│   └── exporter.py     # CSV conversion utility
├── data/
│   └── sample_input.json # Dummy data to test the API
├── tests/
│   └── test_solver.py  # Unit tests for constraint logic
├── requirements.txt    # Python dependencies
└── main.py             # Server entry point

```

---

## 🚀 Installation & Setup

### 1. Prerequisites

Make sure you have **Python 3.8+** installed on your machine.

### 2. Clone/Setup the Repository

Navigate to the folder where you want this project to live and open your terminal.

### 3. Create a Virtual Environment (Recommended)

Keep your dependencies isolated from your system Python.
**Windows:**

```bash
python -m venv venv
.\venv\Scripts\activate

```

**macOS / Linux:**

```bash
python3 -m venv venv
source venv/bin/activate

```

### 4. Install Dependencies

```bash
pip install -r requirements.txt

```

---

## 🏃‍♂️ Running the Server

To start the API engine, run the following command in your terminal:

```bash
python main.py

```

*(Alternatively, you can run: `uvicorn main:app --reload`)*

You should see an output indicating the server is running on `http://127.0.0.1:8000` or `http://0.0.0.0:8000`.

---

## 📖 How to Use the API

FastAPI automatically generates a testing dashboard for you. You do not need Postman or a frontend website to test this engine.

### Step 1: Access the Dashboard

Open your web browser and navigate to:

👉 **[http://localhost:8000/docs](http://localhost:8000/docs)**

### Step 2: Generate a Timetable

1. On the Swagger UI page, click the green **`POST /api/generate`** endpoint to expand it.
2. Click the **"Try it out"** button in the top right corner.
3. Open the `data/sample_input.json` file in your code editor and copy all of its contents.
4. Paste the JSON data into the **Request body** text area on the web page.
5. Click the large blue **"Execute"** button.
6. Scroll down to the **Server response** section to see your generated, clash-free schedule!

### Step 3: Test the CSV Exporter

1. Copy the massive JSON array (`[ { ... }, { ... } ]`) from the `schedule` property of your successful response in Step 2.
2. Scroll down and expand the **`POST /api/export/class/{class_name}`** endpoint.
3. Click **"Try it out"**.
4. In the `class_name` field, type the name of a class exactly as it appears in your data (e.g., `Grade 10A`).
5. In the **Request body**, paste the JSON array you copied from Step 1.
6. Click **Execute**.
7. Click the **"Download file"** link in the response to get your CSV!

---

## 🧪 Running Automated Tests

To mathematically prove that the constraints work and that the engine rejects impossible schedules, run the unit tests:

```bash
python -m unittest tests/test_solver.py

```

You should see `...` and `OK`, indicating all tests passed successfully.

---

## 🧩 Understanding the Data Model (JSON Payload)

When sending data to the `/api/generate` endpoint, your JSON must include:

* **`days_per_week` / `periods_per_day**`: Integers defining the size of the grid.
* **`rooms`**: List of rooms. Must specify `capacity` and `is_lab` (boolean).
* **`teachers`**: List of teachers. Must specify `max_periods_per_week`.
* **`class_groups`**: List of student groups. Must specify `student_count`.
* **`lessons`**: The core requirements tying everything together.
* *Example:* "Teacher T1 must teach Subject X to Class C1 for 4 periods a week, and it requires a lab."



*Check `data/sample_input.json` for a perfectly formatted example.*

```

```
