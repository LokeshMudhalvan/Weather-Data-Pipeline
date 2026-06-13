import psycopg2
from psycopg2 import sql


def connect_to_db(db_name, username, password, host, port):
    conn = None
    try:
        conn = psycopg2.connect(
            database=db_name, user=username, password=password, host=host, port=port
        )
    except Exception as e:
        print("Error connection to db:", e)
    return conn


def check_if_table_exists(conn, table_name):
    command = """
    SELECT * FROM information_schema.tables
    WHERE table_name = %s
    """

    cur = conn.cursor()
    cur.execute(command, (table_name,))

    return bool(cur.rowcount)


def create_table(conn, table_name):
    command = sql.SQL("""
    CREATE TABLE {} (
        id SERIAL PRIMARY KEY,
        timestamp TIMESTAMP NOT NULL, 
        temperature_celcius REAL NOT NULL, 
        temperature_farenheit REAL NOT NULL, 
        weather_info VARCHAR(100) NOT NULL
    )
    """).format(sql.Identifier(table_name))

    try:
        cur = conn.cursor()
        cur.execute(command)
        cur.close()
        conn.commit()
    except Exception as e:
        print("Error creating table:", e)


def insert_weather(conn, data):
    command = """
    INSERT INTO weather_info (
        timestamp,
        temperature_celcius,
        temperature_farenheit,
        weather_info
    )
    VALUES (%s, %s, %s, %s)
    """

    cur = conn.cursor()
    cur.execute(
        command,
        (
            data["date"],
            data["temperatureInCelcius"],
            data["temperatureInFarenheit"],
            data["weatherAlert"],
        ),
    )
    cur.close()
    conn.commit()
