# wsgi.py
from note_app import create_app

# Vercel requires the app variable to be named 'app'
app = create_app()

if __name__ == "__main__":
    app.run()