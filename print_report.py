import psycopg2

"""
1. define a function for each query
2. print information neatly into console
"""
DBNAME = 'news'

def top_three_articles():
    db = psycopg2.connect(database=DBNAME)
    cursor = db.cursor()
    cursor.execute("""
        select count(*) as views, replace(replace(path, '/article/', ''), '-', ' ')
        as title from log group by path order by views desc offset 1 limit 3;
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
                from (select count(*) as views, replace(path, '/article/', '') as slug
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

def requests_days_with_errors():
    pass

print(top_three_articles())
print(list_authors_by_popularity())
