## Getting Started

### Prerequisites
- Python 3.x
- Git

### Setup (laptop)

1. Clone the repo
   git clone <repo-url>
   cd piot-classroom

2. Create and activate virtual environment
   python3 -m venv venv
   source venv/bin/activate        # Mac/Linux
   venv\Scripts\activate           # Windows

3. Install dependencies
   pip install -r requirements.txt

4. Copy the environment file and fill in your values
   cp .env.example .env

### Setup (Raspberry Pi)

Same as above, plus:

   pip install -r requirements-pi.txt

This installs sense-hat on top of the common dependencies.

### Running the project

Make sure you have locally created .env file.

Master Pi:
   cd master_pi
   python app.py

Agent Pi:
   cd agent_pi
   python app.py

Room Pi:
   cd room_pi
   python app.py

### Every time you run your code(important!!)
   source venv/bin/activate

### Adding a new package
   pip install <package-name>
   pip freeze > requirements.txt
   git add requirements.txt
   git commit -m "add <package-name>"

## Demo Day Setup (Multi-Device)

### Before leaving home
- Push all changes to GitHub
- Ensure database is seeded and working

### On the day

**1. Find the Master Pi's IP:**
```bash
hostname -I   # on Master Pi
```

**2. Update `.env` on each device** with the Master Pi's IP:
```
MASTER_PI_IP=192.168.x.x
```

**3. Allow remote DB connections** (run once on the laptop hosting MySQL):
```sql
CREATE USER 'piot_user'@'%' IDENTIFIED BY 'piot_password';
GRANT ALL PRIVILEGES ON piot_db.* TO 'piot_user'@'%';
FLUSH PRIVILEGES;
```

**4. Update `master_pi/db.py`** with the laptop's IP on the day.

**5. Start in order:**
1. MySQL on laptop
2. Mosquitto on Master Pi
3. Master Pi app
4. Room Pi app
5. Agent Pi app

---

# Code Architecture - V1
<img width="1358" height="1258" alt="image" src="https://github.com/user-attachments/assets/6e3a18f3-21c0-4678-a4ea-5d5c1bd628bd" />

