import psycopg2
from config import config
from reddit_json import fetch_json


def insert_posts(posts):
    sql = """INSERT INTO posts(id, score, timestamp)
             VALUES(%s, %s, %s);"""
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.executemany(sql, posts)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return

if __name__ == '__main__':
    insert_posts(fetch_json('..\equelmemes.json'))