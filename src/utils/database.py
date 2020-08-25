import psycopg2
import datetime
import logging
from configparser import ConfigParser

logger = logging.getLogger("utils.database")

db = None


def load_db(_db):
    global db
    db = _db
    return


def insert_posts(posts):
    for post in posts:
        logger.info(f'Adding {post[0]} to database with info {post}')
    sql = """INSERT INTO posts(id, score, timestamp, thousand, author, url, title)
             VALUES(%s, %s, %s, %s, %s, %s, %s);"""
    conn = None
    try:
        params = db
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.executemany(sql, posts)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
    finally:
        if conn is not None:
            conn.close()
    return


def update_scores(posts):
    logger.info('Updating scores in database')
    add_posts = []
    sql = """SELECT * FROM posts WHERE id LIKE %s"""
    sql2 = """UPDATE posts SET score = %s WHERE id LIKE %s"""
    conn = None
    try:
        params = db
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        for post in posts:
            cur.execute(sql, (post[0],))
            if cur.fetchone() is None:
                add_posts.append(post)
            else:
                cur.execute(sql2, (post[1], post[0]))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
    finally:
        if conn is not None:
            conn.close()
    return add_posts


def update_posts():
    logger.info('Marking posts with over 1000 upvotes in database')
    sql = """SELECT * FROM posts WHERE score >= 1000 AND thousand = FALSE"""
    sql2 = """UPDATE posts SET thousand = TRUE WHERE score >= 1000 AND thousand = FALSE"""
    conn = None
    over_threshold = None
    try:
        params = db
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql)
        over_threshold = cur.fetchall()
        cur.execute(sql2)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
    finally:
        if conn is not None:
            conn.close()
    return over_threshold


def remove_posts():
    logger.info('Removing posts over 1 day old from database')
    seconds_since_epoch = int(datetime.datetime.now().timestamp())
    sql = """DELETE FROM posts WHERE %s - timestamp > 86400"""
    conn = None
    try:
        params = db
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql, [seconds_since_epoch])
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error(error)
    finally:
        if conn is not None:
            conn.close()
    return
