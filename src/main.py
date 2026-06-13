import os

from dotenv import load_dotenv

from db import check_if_table_exists, connect_to_db, create_table
from extract import extract_weather_data
from load import load
from transform import transform_weather_data


def main():
    load_dotenv()

    db_name = os.getenv("DB_NAME")
    username = os.getenv("DB_USERNAME")
    password = os.getenv("DB_PASSWORD")
    port = os.getenv("DB_PORT")
    host = os.getenv("DB_HOST", "localhost")
    table_name = os.getenv("TABLE_NAME")

    conn = connect_to_db(db_name, username, password, host, port)

    if conn is None:
        print("Failed to connect to database")
        return

    if not check_if_table_exists(conn, table_name):
        create_table(conn, table_name)

    extracted_df = extract_weather_data()
    transformed_df = transform_weather_data(extracted_df)

    load(conn, transformed_df)

    conn.close()


if __name__ == "__main__":
    main()
