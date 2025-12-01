# Smart Task Manager

## Your Selling Point

A Django-powered REST API with a beautiful web interface that intelligently manages and prioritizes tasks using advanced algorithms. The Smart Task Manager analyzes task dependencies, deadlines, and complexity to provide optimal task ordering and resource allocation.

### Key Features
- **🧠 Intelligent Task Prioritization**: Proprietary algorithm that considers deadlines, dependencies, and complexity
- **👤 User Authentication**: Secure JWT-based login/registration system
- **🎨 Beautiful UI**: Responsive web interface with real-time task management
- **📊 Analytics Dashboard**: Track completion rates, workload metrics, and overdue tasks
- **🚀 Multiple Strategies**: Smart Balance, Deadline-based, Impact-based, and Quick Wins prioritization
- **💡 Smart Recommendations**: AI-powered suggestions to optimize your workflow
- **📱 Fully Responsive**: Works on desktop, tablet, and mobile devices
- **RESTful API**: Full-featured REST API for programmatic access
- **CORS Support**: Ready for third-party frontend integration

## Getting Started

### Prerequisites
- Python 3.8+
- pip

### Installation

1. Create a virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Start the server:
```bash
python manage.py runserver
```

5. Open the web interface:
```
http://localhost:8000/index.html
```

## How to Use

### Web Interface (index.html)
1. **Register/Login**: Create a new account or sign in with existing credentials
2. **Add Tasks**: Fill in the task form with title, deadline, complexity, and priority
3. **View Optimized Order**: See tasks sorted by intelligent algorithm
4. **Choose Strategy**: Select from 4 different prioritization strategies
5. **Track Progress**: Update task status (Start, Complete, Delete)
6. **View Analytics**: Monitor completion rates and workload metrics
7. **Get Recommendations**: Receive AI-powered workflow suggestions

### API Endpoints

**Authentication:**
- `POST /api/auth/login/` - User login
- `POST /api/auth/register/` - Register new user

**Tasks (Requires Authentication):**
- `GET /api/tasks/` - List all user tasks
- `POST /api/tasks/` - Create a new task
- `GET /api/tasks/<id>/` - Retrieve a specific task
- `PUT /api/tasks/<id>/` - Update a task
- `DELETE /api/tasks/<id>/` - Delete a task
- `GET /api/tasks/analyze/` - Get AI-powered task analysis
- `POST /api/tasks/<id>/start/` - Mark task as in progress
- `POST /api/tasks/<id>/complete/` - Mark task as completed
- `POST /api/tasks/<id>/block/` - Mark task as blocked

### Example API Usage

**Login:**
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "user", "password": "pass"}'
```

**Create Task:**
```bash
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Fix Bug",
    "description": "Fix login issue",
    "priority": 4,
    "deadline": "2025-12-31T23:59:59Z",
    "estimated_duration": 3,
    "complexity": 7
  }'
```

## Technology Stack
- **Backend**: Django 4.2.7
- **API**: Django REST Framework 3.14.0
- **Authentication**: djangorestframework-simplejwt 5.5.1
- **CORS**: django-cors-headers 4.3.1
- **Database**: SQLite3
- **Frontend**: Vanilla JavaScript, HTML5, CSS3

## Architecture

```
smart_task_manager/
├── index.html              # Web UI (open in browser)
├── manage.py
├── requirements.txt
├── backend/                # Django config
│   ├── settings.py        # JWT, CORS, REST config
│   ├── urls.py
│   └── wsgi.py
└── tasks/                  # Core app
    ├── models.py          # Task model with user support
    ├── views.py           # REST API viewsets
    ├── serializers.py     # JSON serialization
    ├── urls.py            # API routing
    ├── auth_views.py      # Authentication endpoints
    └── engine.py          # Smart algorithm (The Brain)
```

## The Smart Algorithm (engine.py)

The core intelligence behind the task prioritization:

1. **Priority Weight (40%)**: Direct task importance
2. **Deadline Urgency (35%)**: Time-based scoring (overdue = highest)
3. **Complexity & Duration (15%)**: Task size and difficulty
4. **Dependencies (10%)**: Blocking tasks get boosted scores

**Smart Features:**
- Detects overdue tasks and flags them
- Analyzes workload balance
- Identifies blocking dependencies
- Tracks completion progress
- Generates actionable recommendations

## Creating a User

The first time you run the app, register a new account:

1. Open http://localhost:8000/index.html
2. Click "Register"
3. Enter username, email, and password
4. Start creating tasks!

## Development

### Run Tests
```bash
python manage.py test tasks
```

### Create Superuser
```bash
python manage.py createsuperuser
```

Access admin panel at: `http://localhost:8000/admin/`

### Debug Mode
All features work in development with `DEBUG=True` in settings.py

## Future Enhancements
- [ ] Team collaboration features
- [ ] Recurring tasks
- [ ] Task templates
- [ ] Slack/Teams integration
- [ ] Mobile app
- [ ] Calendar view
- [ ] Time tracking
- [ ] Export reports

## 📸 UI Showcase — Smart Task Manager

Below is the visual preview of all main screens of the Smart Task Manager.

---

### 1️⃣ Homepage  
![Homepage](Images/Homepage.png)

---

### 2️⃣ Smart Sorting  
![Smart](Images/Smart.png)

---

### 3️⃣ Date Sorting  
![Date](Images/Date.png)

---

### 4️⃣ Impact Sorting  
![Impact](Images/Impact.png)

---

### 5️⃣ Quick Session Sorting  
![Quick Session](Images/Quick session.png)
