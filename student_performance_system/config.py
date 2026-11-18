import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key")

    # SQLite works immediately for development. Set DATABASE_URL to a MySQL URL
    # for production, for example:
    # mysql+pymysql://root:password@localhost/student_performance_db
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(BASE_DIR, "database", "student_performance.db").replace("\\", "/")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "reports")
