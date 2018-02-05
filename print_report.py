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
        select count(*) as views, replace(replace(path, '/article/', ''),
        '-', ' ') as title from log group by path order by views desc
        offset 1 limit 3;
    """)
    top_three = cursor.fetchall()
    db.close()
    return top_three


def list_authors_by_popularity():
    db = psycopg2.connect(database=DBNAME)
    cursor = db.cursor()
    cursor.execute("""
        select name, sum(views) as views
            from (select author, views
                from (select count(*) as views, replace(path, '/article/', '')
                as slug
                    from log
                    group by path
                    order by views
                    desc offset 1) as A, articles
                where A.slug = articles.slug) as B, authors
            where B.author = authors.id
            group by name
            order by views desc;
    """)
    author_views = cursor.fetchall()
    db.close()
    return author_views


def request_days_with_errors():
    db = psycopg2.connect(database=DBNAME)
    cursor = db.cursor()
    cursor.execute("""
        select day, round(percentage, 2) as percentage
            from (select B.day, (1.0 * b_occurances / occurances * 100) as
            percentage
                from good_status_by_day as A, bad_status_by_day as B
                where A.day = B.day) as subq
             where percentage > 1;
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

