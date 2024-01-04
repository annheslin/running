import csv
from flask import Flask, render_template, g
import logging
from logging.handlers import RotatingFileHandler
import sqlite3

# Flask app configurations
app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True # tells Flask to automatically reload templates when modified 

# Configure Flask app logger
handler = RotatingFileHandler('flask_app.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

#configure cs50 lib to use sqllite db
conn = sqlite3.connect('nycrunning.db')
cursor = conn.cursor()

# Function to get SQLite connection
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('nycrunning.db')
        g.cursor = g.db.cursor()
    return g.db, g.cursor

# Teardown function to close the SQLite connection
@app.teardown_appcontext
def close_db(error):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/')
def home():
    try:
        # read the column names
        db, cursor = get_db()
        cursor.execute("PRAGMA table_info(running_groups)")
        app.logger.info("Executing query: PRAGMA table_info(running_groups)")

        columns = cursor.fetchall()
        
        # Check if columns is empty (indicating an issue with the query)
        if not columns:
            app.logger.error("Error fetching column information. Check your query.")
            return "Error fetching column information. Check your query."

        column_names = [column[1] for column in columns]

        # define each row in the runninggroup 
        cursor.execute("SELECT * FROM running_groups")
        group = cursor.fetchall()

        # added by gpt:
        app.logger.info(f"Columns: {column_names}")
        app.logger.info(f"Group: {group}")

        # table_data should be reference in html file

        return render_template('layout.html', group=group, columns=column_names) 

    except Exception as e:
        app.logger.error(f"An error occurred: {str(e)}")
        return "An error occurred."


if __name__ == "__main__":
    app.run(debug=False, port=int(os.environ.get("PORT", 5000)))

