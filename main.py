import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flasgger import Swagger

load_dotenv()

app = Flask(__name__)

# swagger alustus tässä
Swagger(app, template={
    "info": {
        "title": "OpenAQ API",
        "description": "Ilmanlaatudatan haku REST-rajapinnasta\n\nTekijä: Sammeli Näkkäläjärvi",
        "version": "1.0.0",
        }
})

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
    # Flasgger dokumentaatio testi
    """
    Yhden päivän mittaukset halutulle mittauspisteelle.
    ---
    tags:
        - Mittaukset
    parameters:
      - name: location_id
        in: path
        type: integer
        required: true
        description: OpenAQ location id
      - name: day
        in: path
        type: string
        required: true
        description: Päivämäärä muodossa YYYY-MM-DD
    responses:
      200:
        description: Lista mittauksista
      404:
        description: Ei mittauksia
    """

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
    """
    Listaa kaikki mittauspisteet.
    ---
    tags:
        - Mittaukset
    responses:
        200:
            description: Lista mittauksista
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT openaq_id, name FROM locations")
            rows = cur.fetchall()
    return jsonify(rows)
@app.route("/test2")

# tarkistetaan päivämäärä, koska aluksi ei tullut mitään.
def test2():
    """
    Hae päivämäärä datasta.
    ---
    tags:
        - Mittaukset
    responses:
        200:
            description: Lista dataan sisälletyistä päivämääristä
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT measured_at FROM measurements LIMIT 3")
            rows = cur.fetchall()
    return jsonify(rows)

# tällä voidaan hakea valitun mittauspaikan mittausten lukumäärät
@app.route("/measurements/<int:location_id>/count")
def get_measurement_count(location_id):
    """
    Hakee kaikkien mittausten lukumäärät valitulta mittauspaikalta.
    ---
    tags:
        - Mittaukset
    parameters:
      - name: location_id
        in: path
        type: integer
        required: true
        description: OpenAQ location id
    responses:
      200:
        description: Mittausten lukumäärä
      404:
        description: Ei mittauksia
    """
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT COUNT(*) AS count
                FROM measurements m
                JOIN sensors s ON s.id = m.sensor_id
                JOIN locations l ON l.id = s.location_id
                WHERE l.openaq_id = %s
            """, (location_id,))
            row = cur.fetchone()

    return jsonify(row)

# laskee mittauspaikan ja anturin mittauskeskiarvot yhdelle päivälle
@app.route("/measurements/<int:location_id>/daily-avg")
def get_daily_avg(location_id):
    """
    Laskee mittauspaikan ja valitan anturin mittauskeskiarvot aina yhdelle päivälle.
    ---
    tags:
      - Mittaukset
    parameters:
      - name: location_id
        in: path
        type: integer
        required: true
        description: OpenAQ location id
      - name: day
        in: query
        type: string
        required: true
        description: Päivämäärä muodossa YYYY-MM-DD
      - name: parameter
        in: query
        type: string
        required: true
        description: Kuvaa käytössä olevaa anturia. Esim. pm10, no2 ja o3
    responses:
      200:
         description: Mittausten keskiarvo
      404:
         description: Ei mittauksia
    """
    day = request.args.get("day")
    parameter = request.args.get("parameter")

    if not day or not parameter:
        return jsonify({"error": "Päivä ja parametri vaaditaan."}), 400

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT AVG(m.value) AS avg_value, COUNT(*) AS count,
                       p.name AS parameter, p.unit
                FROM measurements m
                JOIN sensors s ON s.id = m.sensor_id
                JOIN parameters p ON p.id = s.parameter_id
                JOIN locations l ON l.id = s.location_id
                WHERE l.openaq_id = %s
                  AND p.name = %s
                  AND m.measured_at >= %s::date
                  AND m.measured_at < %s::date + INTERVAL '1 day'
                GROUP BY p.name, p.unit
            """, (location_id, parameter, day, day))
            row = cur.fetchone()

    if not row:
        return jsonify({"error": "Ei mittauksia."}), 404

    return jsonify(row)

if __name__ == "__main__":
    app.run(debug=True)