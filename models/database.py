import sqlite3
import hashlib
import os

# ── Database path ─────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS farmers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            mobile TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_id INTEGER NOT NULL,
            report_type TEXT NOT NULL,
            inputs TEXT NOT NULL,
            result TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (farmer_id) REFERENCES farmers(id)
        )
    """)

    conn.commit()
    conn.close()
    print("Database initialised successfully!")


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def register_farmer(name, email, password, mobile):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO farmers (name, email, password_hash, mobile) VALUES (?, ?, ?, ?)",
            (name, email, hash_password(password), mobile)
        )

        conn.commit()
        return True, "Registration successful!"

    except sqlite3.IntegrityError:
        return False, "This email is already registered. Please log in."

    finally:
        conn.close()


def login_farmer(email, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, name, email, mobile FROM farmers WHERE email=? AND password_hash=?",
        (email, hash_password(password))
    )

    row = cursor.fetchone()
    conn.close()

    if row:
        return {
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "mobile": row[3]
        }

    return None


def save_report(farmer_id, report_type, inputs, result):
    import json

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO reports (farmer_id, report_type, inputs, result) VALUES (?, ?, ?, ?)",
        (farmer_id, report_type, json.dumps(inputs), result)
    )

    conn.commit()
    conn.close()


def get_farmer_reports(farmer_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT report_type, inputs, result, created_at
        FROM reports
        WHERE farmer_id=?
        ORDER BY created_at DESC
        """,
        (farmer_id,)
    )

    rows = cursor.fetchall()
    conn.close()

    return rows


def get_all_farmers():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, name, email, mobile, created_at
        FROM farmers
        ORDER BY created_at DESC
        """
    )

    rows = cursor.fetchall()
    conn.close()

    return rows


def get_all_reports():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            farmers.name,
            farmers.email,
            reports.report_type,
            reports.inputs,
            reports.result,
            reports.created_at
        FROM reports
        JOIN farmers
        ON reports.farmer_id = farmers.id
        ORDER BY reports.created_at DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows

def get_stats_summary():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM farmers")
    farmers_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM reports")
    reports_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM reports WHERE report_type='soil'")
    soil_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM reports WHERE report_type='pest'")
    pest_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM reports WHERE report_type='crop'")
    crop_count = cursor.fetchone()[0]

    conn.close()

    return {
        "farmers": farmers_count,
        "reports": reports_count,
        "soil": soil_count,
        "pest": pest_count,
        "crop": crop_count
    }


def delete_farmer(farmer_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM reports WHERE farmer_id=?",
        (farmer_id,)
    )

    cursor.execute(
        "DELETE FROM farmers WHERE id=?",
        (farmer_id,)
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
    print(f"Database created at: {DB_PATH}")