echo on

for /F "tokens=2 delims=:" %%i in ('"ipconfig | findstr IP | findstr 192."') do SET LOCAL_IP=%%i

start chrome %LOCAL_IP%

call venv\Scripts\activate.bat

set FLASK_APP=app.py

set FLASK_ENV=development


flask run --host=0.0.0.0 --port=80

pause

