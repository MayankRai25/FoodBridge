@echo off
echo Starting FoodBridge Flask Server...
echo.

echo Installing required packages...
pip install flask flask-sqlalchemy flask-cors

echo.
echo Starting Flask application...
python app.py

pause