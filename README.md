# Database reporting tool
I've been asked to build an internal reporting tool that will use information from the database to discover what kind of articles the site's readers like.

The database contains newspaper articles, as well as the web server log for the site. The log has a database row for each time a reader loaded a web page. Using that information, I've answers questions about the site's user activity.

The database is running on PostgreSQL.

## Usage instructions
On the server where the DB is running execute the following command
`python3 print_report.py`

### Questions answered:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

### Database views
**status_by_day**
```
SELECT count(log.status) AS occurances,
  log."time"::date AS day,
  log.status
 FROM log
GROUP BY log.status, (log."time"::date)
ORDER BY (log."time"::date) DESC;
```

**good_status_by_day**
```
SELECT status_by_day.occurances,
  status_by_day.day,
  status_by_day.status
 FROM status_by_day
WHERE status_by_day.status = '200 OK'::text;
```

**bad_status_by_day**
```
SELECT status_by_day.occurances AS b_occurances,
  status_by_day.day,
  status_by_day.status
 FROM status_by_day
WHERE status_by_day.status <> '200 OK'::text;
```
