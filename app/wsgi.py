from app import app, create_tables

create_tables()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 5000, debug = True)