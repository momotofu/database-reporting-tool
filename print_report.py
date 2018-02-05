import psycopg2
from table_str import format_row

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


def print_result(message, col_names, list_of_tup):
    print(message)
    output_list = []
    col_width = 0
    padding = 3

    # find logest col
    for item in list_of_tup:
        for item_a in item:
            width = len(str(item_a))
            if width > col_width:
                col_width = width

    # Add column labels
    output_list.append(format_row(col_names, True, col_width + padding))
    for item in list_of_tup:
        row_items = []
        for item_a in item:
            row_items.append(item_a)
        output_list.append(format_row(row_items, None, col_width + padding))

    for item in output_list:
        print(item)

print_result('Top three articles: ', ['views', 'article title'], top_three_articles())
# top_three_articles())
# list_authors_by_popularity())
# request_days_with_errors())

# status_by_day
# bad_status_by_day
# good_status_by_day
