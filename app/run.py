# run.py
from app import create_app, create_tables

app = create_app()
create_tables()

if __name__ == '__main__':
    app.run(debug=True)