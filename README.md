# Database reporting tool
This is an internal reporting tool that uses information from the database (PostgreSQL) to discover what kind of articles the site's readers like.

The database contains newspaper articles, slugs, authors etc. as well as the server log for the site. The log has a records row for each time a reader loaded a web page and contains user path, ip, HTTP method, status, time, and user id.

**The following statistics were discovered.**
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## Usage instructions
This tool requires creating SQL views and is run on ubuntu-16.04-i386.
For information on the psql CLI see [psql documentation](https://www.postgresql.org/docs/current/static/app-psql.html).

1. login to the server and connect to the news database using: `psql news`
2. copy and paste the following view creation commands into your
   terminal.

**status_by_day**
```
CREATE VIEW status_by_day as SELECT count(status) AS occurances,
  CAST(time AS DATE) as day, status
 FROM log
GROUP BY status, day
ORDER BY day DESC;
```

**good_status_by_day**
```
CREATE VIEW good_status_by_day as SELECT occurances,
  day,
  status
 FROM status_by_day
WHERE status = '200 OK';
```

**bad_status_by_day**
```
CREATE VIEW bad_status_by_day as SELECT occurances AS b_occurances,
  day,
  status
 FROM status_by_day
WHERE status != '200 OK';
```
3. Execute the following command: `python3 print_report.py`

Below is an example output:
```
Top three articles:
===================================================
||         views         |     article title     ||
===================================================
||         338647        |   candidate is jerk   ||
---------------------------------------------------
||         253801        |   bears love berries  ||
---------------------------------------------------
||         170098        |    bad things gone    ||
---------------------------------------------------


Authors by popularity:
===========================================================
||        author name        |           views           ||
===========================================================
||      Ursula La Multa      |           507594          ||
-----------------------------------------------------------
||   Rudolf von Treppenwitz  |           423457          ||
-----------------------------------------------------------
||   Anonymous Contributor   |           170098          ||
-----------------------------------------------------------
||       Markoff Chaney      |           84557           ||
-----------------------------------------------------------


Days with errors over 1%:
======================================
||      day      | error percentage ||
======================================
||   2016-07-17  |      2.32        ||
--------------------------------------

```

## Design considerations
All statistics are queried by a single SQL query, leaving the heavy
lifting to the database (minimal python "post-processing"). As a result
some database views were created.

The code was kept clean and modular by separating printing functions into
their own module `table_str.py`, and by conforming to Pep8 guidelines.
