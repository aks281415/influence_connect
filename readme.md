# InfluenceConnect

This platform bridges the gap between **Sponsors** and **Influencers**. It allows sponsors to connect with influencers to advertise their products or services while enabling influencers to earn monetary benefits for their promotions.

## Features

### Role-Based Access Control (RBAC)
- Secure login for Admin, Sponsors, and Influencers with JWT-based authentication

### Admin Dashboard
- Manage user approvals
- Monitor flagged accounts
- View application statistics (active users campaigns, etc.)

### Campaign Management
- Sponsors can create, update, and delete campaigns and ad requests

### Influencer Tools
- Influencers can view, accept/reject, or negotiate ad requests
- Search for public campaigns

### Automated Reminders & Reports
- Daily reminders for pending tasks
- Monthly activity reports for sponsors

### Performance Optimization
- Caching and async jobs for improved API performance
- CSV exports for campaign details

## Getting Started

### 1. Create Virtual Environment (Open New Terminal)
```
# Linux/MacOS
python3 -m venv myenv

# Windows
python -m venv venv
```

### 2. Activate Virtual Environment
```
# Linux/MacOS
source myenv/bin/activate

# Windows
venv\Scripts\activate

python app.py
```

### 3. Requirements
To install Python dependencies, navigate to the backend folder and run:
```
pip install -r requirements.txt
```

### 4. Frontend Setup (Open New Terminal)
```
cd frontend
npm install
npm run serve
```

### 5. Redis Commands (Open New Terminal)
```
# Start Redis Server
sudo service redis-server start

# Access Redis CLI
redis-cli

# View All Keys
KEYS *

# Stop Redis Server
sudo service redis stop

# Shutdown Redis via CLI
redis-cli shutdown
```

### 6. Celery Commands (Open New Terminal)
```
# Start Celery Worker
celery -A tasks worker --loglevel=info

# Start Celery Beat Scheduler (Open Another New Terminal)
celery -A tasks beat --loglevel=info
```