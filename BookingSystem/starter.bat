echo on

start chrome "127.0.0.1"

call venv\Scripts\activate.bat

set FLASK_APP=app.py

set FLASK_ENV=development

flask run --port=80



