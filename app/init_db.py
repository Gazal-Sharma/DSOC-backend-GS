# init_db.py
from app import create_app, db, create_tables

app = create_app()

with app.app_context():
    db.create_all()

print("Database initialized successfully")

if __name__ == "__main__":
    app = create_app()
    create_tables()
    app.run(debug = True)