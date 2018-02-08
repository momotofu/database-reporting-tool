#!/usr/bin/env python3
import psycopg2


from table_str import format_row, print_result_table
"""
queries the news database

Views created in db:
status_by_day
bad_status_by_day
good_status_by_day
"""

DBNAME = 'news'


def connect(db_name):
    """
    Connect to the PostgreSQL database. Returns a databse connection.
    """
    try:
        db = psycopg2.connect(database=db_name)
        c = db.cursor()
        return db, c
    except psycopg2.Error as e:
        print("Unable to connect to database with exception {}".format(e))
        sys.exit(1)


def execute_query(query, connection):
    db, c = connection
    c.execute(query)
    db.commit()
    result = c.fetchall()
    db.close()
    return result


print_result_table(
    'Top three articles: ',
    ['views', 'article title'],
    execute_query("""
        SELECT COUNT(*) as VIEWS, REPLACE(REPLACE(path, '/article/', ''),
        '-', ' ') AS title
            FROM log
            GROUP BY path
            ORDER by views DESC
            OFFSET 1 LIMIT 3;
    """, connect(DBNAME))
    )
print_result_table(
    'Authors by popularity: ',
    ['author name', 'views'],
    execute_query("""
        SELECT name, SUM(views) AS views
            FROM (SELECT author, views
                FROM (SELECT COUNT(*) AS views, REPLACE(path, '/article/', '')
                AS slug
                    FROM log
                    GROUP BY path
                    ORDER BY views DESC OFFSET 1) AS A, articles
                WHERE A.slug = articles.slug) AS B, authors
            WHERE B.author = authors.id
            GROUP BY name
            ORDER BY views DESC;
    """, connect(DBNAME))
    )
print_result_table(
    'Days with errors over 1%: ',
    ['day', 'error percentage'],
    execute_query("""
        SELECT day, ROUND(percentage, 2) AS percentage
            FROM (SELECT B.day, (1.0 * b_occurances / occurances * 100) AS
            percentage
                FROM good_status_by_day AS A, bad_status_by_day AS B
                WHERE A.day = B.day) AS subq
             WHERE percentage > 1;
        """, connect(DBNAME))
    )
