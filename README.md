# Capstone TaskFlow

A full-stack Task Management application built for the Capstone Project.

## Features
- User, Project and Task management
- Full CRUD for Tasks
- Project statistics using SQL aggregation
- Custom Insertion Sort and Binary/Linear Search
- AI Quick-Add (rule-based mock parser)
- Responsive frontend dashboard with localStorage caching

## Tech Stack
- Backend: FastAPI, SQLAlchemy, SQLite
- Frontend: HTML, CSS, JavaScript
- Algorithms: Hand-written Insertion Sort, Binary Search, Linear Search

## Project Structure capstone-taskflow/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── algorithms.py
│   │   ├── ai_parser.py
│   │   └── routers/
│   └── requirements.txt
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── script.js
└── README.md 
## How to Run Locally
### 1. Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload   
Backend runs at: http://127.0.0.1:8000
API Docs: http://127.0.0.1:8000/docs 
2. Frontend
Open frontend/index.html in your browser
(or use Live Server on port 5500)
First Time Setup

Create a User using POST /users/
Create a Project using POST /projects/ (use owner_id = 1)
Then you can add tasks from the frontend or API  
## API Endpoints
### Users
- `POST /users/` → Create user
- `GET /users/` → List users

### Projects
- `POST /projects/` → Create project
- `GET /projects/` → List projects
- `GET /projects/stats` → Project task statistics (SQL aggregation)

### Tasks
- `POST /tasks/` → Create task
- `GET /tasks/` → List all tasks
- `GET /tasks/{id}` → Get task by ID
- `PUT /tasks/{id}` → Update task
- `DELETE /tasks/{id}` → Delete task
- `GET /tasks/sorted?sort=priority` → Sorted tasks using Insertion Sort
- `GET /tasks/search?title=...&algo=binary` → Search using Binary or Linear Search
- `POST /tasks/quick-add` → AI Quick-Add (mock parser)   
## Algorithms (Section 2)
### Implemented Functions
- `insertion_sort(records, key)` – sorts list of dictionaries in-place
- `binary_search(sorted_records, target_value, key)` – returns index or -1
- `linear_search(records, target_value, key)` – returns index or -1

### Complexity
- Insertion Sort: Best O(n), Worst O(n²)
- Binary Search: O(log n)
- Linear Search: O(n)

### Why sorting first can be worth it
Teams list and sort tasks many times per day but add/rename tasks less frequently. Paying the cost of insertion sort once allows subsequent binary searches to be much faster (O(log n) vs O(n)). For small-to-medium task lists this trade-off is acceptable.

## AI Quick-Add (Section 3)

The `/tasks/quick-add` endpoint uses a deterministic rule-based mock parser (no API keys required).

### Prompting Technique
The system uses a **zero-shot** style instruction structure (system role describing the parsing rules + user role carrying the free-text description). This keeps token usage low and makes the behavior fully predictable.

### Example Inputs and Outputs

1. Input: `"Finish the report next Friday, it's urgent"`  
   → title: `"Finish the report , it's"`, priority: `"high"`, due_date: `"next friday"`

2. Input: `"This is urgent, mark it ASAP please"`  
   → title: `"This is , mark it please"`, priority: `"high"`, due_date: `null`

3. Input: `"whenever you can review the design"`  
   → title: `"you can review the design"`, priority: `"low"`, due_date: `null`

4. Input: `"tomorrow review tomorrow"`  
   → title: `"review"`, priority: `"medium"`, due_date: `"tomorrow"`

5. Input: `"   "` (whitespace only)  
   → title: `"Untitled task"`, priority: `"medium"`, due_date: `null`  
## Benchmark Results (Comparison Counts)
## Benchmark Results (Comparison Counts)

Data Size: 10 tasks
- Insertion Sort comparisons: ~28
- Binary Search comparisons: 3–4
- Linear Search comparisons: 10

Data Size: 100 tasks
- Insertion Sort comparisons: ~2,450
- Binary Search comparisons: 6–7
- Linear Search comparisons: 100

Data Size: 500 tasks
- Insertion Sort comparisons: ~62,000
- Binary Search comparisons: 8–9
- Linear Search comparisons: 500

### Analysis
Insertion sort becomes expensive as the number of tasks grows (O(n²)). However, once the list is sorted, binary search is significantly faster than linear search. In normal team usage, tasks are viewed and filtered many times per day while new tasks are added less often. Therefore, the cost of sorting is acceptable because it enables much faster repeated searches.
## Author
## Author

- Name: Chirag Bhatia
- Course: Software Development Engineering With Applied AI
- Institution: Vishleshan i-Hub, IIIT Patna
- Capstone Project - 2026