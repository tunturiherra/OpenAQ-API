import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
from flask import Flask, jsonify

load_dotenv()

app = Flask(__name__)

def get_conn():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PWD"),
        cursor_factory=RealDictCursor
    )

# endpoint tietojen hakemiseksi päivämäärän perusteella
@app.route("/measurements/<int:location_id>/day/<string:day>")
def get_day_measurements(location_id, day):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT m.measured_at, m.value, p.name AS parameter, p.unit
                FROM measurements m
                JOIN sensors s ON s.id = m.sensor_id
                JOIN parameters p ON p.id = s.parameter_id
                JOIN locations l ON l.id = s.location_id
                WHERE l.openaq_id = %s
                  AND m.measured_at >= %s::date
                  AND m.measured_at < %s::date + INTERVAL '1 day'
                ORDER BY m.measured_at
            """, (location_id, day, day))
            rows = cur.fetchall()

    if not rows:
        return jsonify({"error": "Ei mittauksia."}), 404

    return jsonify(rows)

# testataan tietokantayhteyttä
@app.route("/test")
def test():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT openaq_id, name FROM locations")
            rows = cur.fetchall()
    return jsonify(rows)
@app.route("/test2")

# tarkistetaan päivämäärä, koska aluksi ei tullut mitään.
def test2():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT measured_at FROM measurements LIMIT 3")
            rows = cur.fetchall()
    return jsonify(rows)

if __name__ == "__main__":
    app.run(debug=True)