echo on
echo "This is a booking system based on Flask and Python on your own device"

pause

call venv\Scripts\activate.bat

set FLASK_APP=app.py
set FLASK_ENV=development
flask run --host=0.0.0.0

echo "finish"

pause