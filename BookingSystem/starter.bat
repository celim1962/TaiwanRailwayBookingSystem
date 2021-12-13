echo on

call venv\Scripts\activate.bat

set FLASK_APP=app.py

set FLASK_ENV=development

flask run --host=0.0.0.0 --port=80

echo "finish"

pause