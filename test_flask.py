#!/usr/bin/env python3

print("Testing Flask setup...")

try:
    import flask
    print("✓ Flask is installed")
except ImportError:
    print("✗ Flask not installed. Run: pip install flask")
    exit(1)

try:
    import flask_sqlalchemy
    print("✓ Flask-SQLAlchemy is installed")
except ImportError:
    print("✗ Flask-SQLAlchemy not installed. Run: pip install flask-sqlalchemy")
    exit(1)

try:
    import flask_cors
    print("✓ Flask-CORS is installed")
except ImportError:
    print("✗ Flask-CORS not installed. Run: pip install flask-cors")
    exit(1)

print("\nAll dependencies are installed!")
print("Now run: python app.py")