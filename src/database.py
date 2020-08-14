import psycopg2
import datetime
from src import config
from reddit_json import fetch_json


def insert_posts(posts):
    #print('inserting')
    sql = """INSERT INTO posts(id, score, timestamp)
             VALUES(%s, %s, %s);"""
    conn = None
    try:
        # read database configuration
        params = config.config()
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


def check_posts(posts):
    #print('checking')
    add_posts = []
    sql = """SELECT * FROM posts WHERE id LIKE %s"""
    sql2 = """UPDATE posts SET score = %s WHERE id LIKE %s"""
    conn = None
    try:
        params = config.config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        for post in posts:
            #print(post)
            #print(post[0])
            cur.execute(sql, (post[0],))
            if cur.fetchone() is None:
                add_posts.append(post)
            else:
                #print('updating ' + post[0])
                cur.execute(sql2, (post[1], post[0]))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return add_posts


def update_posts():
    #print('updating')
    sql = """SELECT id FROM posts WHERE score >= 1000 AND thousand = FALSE"""
    sql2 = """UPDATE posts SET thousand = TRUE WHERE score >= 1000 AND thousand = FALSE"""
    conn = None
    over_threshold = None
    try:
        params = config.config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql)
        over_threshold = cur.fetchall()
        cur.execute(sql2)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return over_threshold


def remove_posts():
    print('removing')
    seconds_since_epoch = int(datetime.datetime.now().timestamp())
    sql = """DELETE FROM posts WHERE %s - timestamp > 86400"""
    conn = None
    try:
        params = config.config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, seconds_since_epoch)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return
