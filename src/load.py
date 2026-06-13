from db import insert_weather


def load(conn, df):
    for index, row in df.iterrows():
        insert_weather(conn, row)
