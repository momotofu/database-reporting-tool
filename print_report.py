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


def top_three_articles():
    db = psycopg2.connect(database=DBNAME)
    cursor = db.cursor()
    cursor.execute("""
        SELECT COUNT(*) as VIEWS, REPLACE(REPLACE(path, '/article/', ''),
        '-', ' ') AS title
        FROM log
        GROUP BY path
        ORDER by views DESC
        OFFSET 1 LIMIT 3;
    """)
    top_three = cursor.fetchall()
    db.close()
    return top_three


def list_authors_by_popularity():
    db = psycopg2.connect(database=DBNAME)
    cursor = db.cursor()
    cursor.execute("""
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
    """)
    author_views = cursor.fetchall()
    db.close()
    return author_views


def request_days_with_errors():
    db = psycopg2.connect(database=DBNAME)
    cursor = db.cursor()
    cursor.execute("""
        SELECT day, ROUND(percentage, 2) AS percentage
            FROM (SELECT B.day, (1.0 * b_occurances / occurances * 100) AS
            percentage
                FROM good_status_by_day AS A, bad_status_by_day AS B
                WHERE A.day = B.day) AS subq
             WHERE percentage > 1;
        """)
    result = cursor.fetchall()
    db.close()
    return result


print_result_table(
    'Top three articles: ',
    ['views', 'article title'],
    top_three_articles()
    )
print_result_table(
    'Authors by popularity: ',
    ['author name', 'views'],
    list_authors_by_popularity()
    )
print_result_table(
    'Days with errors over 1%: ',
    ['day', 'error percentage'],
    request_days_with_errors()
    )
