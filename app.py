from flask import Flask, render_template
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.event_routes import event_bp

app = Flask(__name__)
app.template_folder = "templates"
app.static_folder = "static"

# Define what they user should see when they visit the root URL
@app.route("/")
def index():
    return render_template("index.html")

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(event_bp)

# Fetch latest events at app startup (dev convenience only)
from utils.event_scraper import CampusEventScraper
import sqlite3
def should_scrape_events():
    try:
        conn = sqlite3.connect("db/campusconnect.db")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM external_events")
        count = cursor.fetchone()[0]
        conn.close()
        return count == 0
    except Exception as e:
        print(f"Skipping scraping: {e}")
        return False

if should_scrape_events():
    scraper = CampusEventScraper("https://www.adrian.edu/calendar", db_path="db/campusconnect.db")
    scraper.run()

if __name__ == "__main__":
    app.run(debug=True)