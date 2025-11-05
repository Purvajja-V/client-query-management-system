# db_utils.py
from sqlalchemy import create_engine, text
import pandas as pd
import hashlib
from datetime import datetime
from urllib.parse import quote_plus

# === CONFIG - change if needed ===
DB_USER = "root"
DB_PASS = "Root@27"            # your MySQL password
DB_HOST = "localhost"
DB_PORT = 3306
DB_NAME = "client_queries_db"


# Build SQLAlchemy URL and engine (URL-encode password)
db_pass_esc = quote_plus(DB_PASS)
DB_URL = f"mysql+mysqlconnector://{DB_USER}:{db_pass_esc}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create engine with pool pre-ping so connections handle transient disconnects
engine = create_engine(DB_URL, pool_pre_ping=True, future=True)

def _hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def ensure_users_table():
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                username VARCHAR(255) PRIMARY KEY,
                password_hash TEXT,
                role VARCHAR(50)
            )
        """))

def ensure_queries_table():
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS queries (
                query_id INT AUTO_INCREMENT PRIMARY KEY,
                mail_id VARCHAR(255),
                mobile_number VARCHAR(50),
                query_heading VARCHAR(255),
                query_description TEXT,
                status VARCHAR(50),
                query_created_time DATETIME,
                query_closed_time DATETIME
            )
        """))

def init_db():
    """Create tables if missing and ensure a support account exists."""
    ensure_users_table()
    ensure_queries_table()
    # create a fixed support account (if not exists)
    # change these creds if you want different support id/password
    create_support_account("support@example.com", "Support@123")

def create_support_account(username: str, password: str):
    """Create the fixed support account only if it doesn't exist."""
    with engine.begin() as conn:
        row = conn.execute(text("SELECT username FROM users WHERE username=:u"), {"u": username}).fetchone()
        if row is None:
            conn.execute(text("INSERT INTO users (username, password_hash, role) VALUES (:u, :p, :r)"),
                         {"u": username, "p": _hash(password), "r": "Support"})

def register_user(username: str, password: str, role: str) -> bool:
    """Register only clients. Returns True if created, False if user exists or role denied."""
    if role != "Client":
        return False
    with engine.begin() as conn:
        row = conn.execute(text("SELECT username FROM users WHERE username=:u"), {"u": username}).fetchone()
        if row:
            return False
        conn.execute(text("INSERT INTO users (username, password_hash, role) VALUES (:u, :p, :r)"),
                     {"u": username, "p": _hash(password), "r": role})
    return True

def authenticate_user(username: str, password: str):
    """Return tuple (status, role) where status in {'invalid_user','wrong_password','success'}."""
    with engine.connect() as conn:
        row = conn.execute(text("SELECT password_hash, role FROM users WHERE username=:u"), {"u": username}).fetchone()
    if row is None:
        return "invalid_user", None
    stored_hash, role = row
    if _hash(password) == stored_hash:
        return "success", role
    else:
        return "wrong_password", None

def update_password(username: str, new_password: str) -> bool:
    """Update password for an existing user. Return True if updated, False if user missing."""
    with engine.begin() as conn:
        res = conn.execute(text("SELECT username FROM users WHERE username=:u"), {"u": username}).fetchone()
        if res is None:
            return False
        conn.execute(text("UPDATE users SET password_hash=:p WHERE username=:u"),
                     {"p": _hash(new_password), "u": username})
    return True

def add_query(mail, mobile, heading, desc):
    with engine.begin() as conn:
        conn.execute(text("""
            INSERT INTO queries (mail_id, mobile_number, query_heading, query_description, status, query_created_time)
            VALUES (:m, :mob, :h, :d, 'Open', :t)
        """), {"m": mail, "mob": mobile, "h": heading, "d": desc, "t": datetime.now()})

def get_all_queries():
    with engine.connect() as conn:
        df = pd.read_sql("SELECT * FROM queries ORDER BY query_created_time DESC", conn)
    return df

def get_open_queries():
    with engine.connect() as conn:
        df = pd.read_sql("SELECT * FROM queries WHERE status='Open' ORDER BY query_created_time DESC", conn)
    return df

def close_query(query_id):
    with engine.begin() as conn:
        conn.execute(text("""
            UPDATE queries
            SET status='Closed', query_closed_time=:t
            WHERE query_id=:id
        """), {"t": datetime.now(), "id": int(query_id)})
