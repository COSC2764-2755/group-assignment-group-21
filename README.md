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

Master Pi:
   cd master_pi
   python app.py

Agent Pi:
   cd agent_pi
   python app.py

Room Pi:
   cd room_pi
   python app.py

### Every time you return to work
   source venv/bin/activate

### Adding a new package
   pip install <package-name>
   pip freeze > requirements.txt
   git add requirements.txt
   git commit -m "add <package-name>"
