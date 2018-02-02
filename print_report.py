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
    pass

def requests_days_with_errors():
    pass

print(top_three_articles())
