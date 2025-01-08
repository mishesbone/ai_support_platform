# ai_support_platform/wsgi.py
from app import create_app

app = create_app("config.DevelopmentConfig")  # You can change to ProductionConfig if needed

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
