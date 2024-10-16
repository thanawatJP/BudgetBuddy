# Virtual Environment (Window)
## Install
```
py -m venv myvenv
```
## Enable
```
myvenv\Scripts\activate.bat
```

# Install all package
```
pip install -r requirements.txt
```

# Go in side project
```
cd budgetbuddy
```

# DB
- Create DB in pgAdmin
- Create Database name budgetbuddy
- Setup in setting.py in database change your password

# Migrate
```
py manage.pt migrate
```

# Run server
```
py manage.py runserver
```
