# Project 3: Log Analysis Project
# geraldgsh
## Udacity Full Stack Nanodegree

#### Objective

Build an internal reporting tool that will use information from the database to discover what kind of articles the site's readers like.

The database contains mock newspaper articles, as well as the web server log for the site. The log has a database row for each time a reader loaded a web page. Using that information, write a code that will answer specific query about the site's user activity.

The written program will run from command line. It won't take any input from the user. Instead, it will connect to that database, use SQL queries to analyze the log data, and print out the responeses to 3 queries;

1. What are the most popular three articles of all time? Which articles have been accessed the most? Present this information as a sorted list with the most popular article at the top.

2. Who are the most popular article authors of all time? That is, when you sum up all of the articles each author has written, which authors get the most page views? Present this as a sorted list with the most popular author at the top.

3. On which days did more than 1% of requests lead to errors? The log table includes a column status that indicates the HTTP status code that the news site sent to the user's browser. 

#### Programs used to execute written code;

  1. [Python Version 2.7.13](https://www.python.org/)
  2. [Vagrant Version 1.9.1](https://www.vagrantup.com/)
  3. [VirtualBox Version 5.1.28 ](https://www.virtualbox.org/)
  4. [Git Version 2.14.1](https://git-scm.com/)

#### Project Setup;
   
  1. Download the [SQL database](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) from here.
  2. Unzip this file.
  3. Copy the newsdata.sql file to local project repository folder.


#### To run the code;

1. Open a Unix-like command line terminal (e.g. Git Bash on Windows), and navigate to the folder containing this project's files.

2. Start VM using the following command;

        $ vagrant up

3. Login VM using the following command;

        $ vagrant ssh

4. Change directory using the following command;

        $ cd /vagrant


#### Initializing database and view table creation

1.Load database (newsdata.sql) with the following command;

        psql -d news -f newsdata.sql

2.Connect to database with the following command;

        psql -d news

3.Create article view table for question 2 with the following command;


        CREATE VIEW viewer AS
        SELECT author, count(path) AS views
        FROM articles, log
        WHERE articles.slug = substring(log.path, 10, 100)
        GROUP BY author
        ORDER BY views DESC LIMIT 4;


To form viewer table below;

    | Column |  Type   | Modifiers | 
    |--------+---------+-----------|
    | author | integer |           |
    | views  | bigint  |           |

    

4.Create error status view table for question 3 with the following command;

Execute the following total_table view command;

        CREATE VIEW total_table AS
        SELECT date(time), COUNT(*) AS views
        FROM log
        GROUP BY date(time)
        ORDER BY date(time);

To form total_table table below;

    | Column |  Type  | Modifiers |
    |--------+--------+-----------|
    | date   | date   |           |
    | views  | bigint |           |


Execute the following error_table view command;

        CREATE VIEW error_table AS
        SELECT date(time), COUNT(*) AS errors
        FROM log WHERE status = '404 NOT FOUND'
        GROUP BY date(time)
        ORDER BY date(time);

To form error_table table below;

    | Column |  Type  | Modifiers |
    |--------+--------+-----------|
    | date   | date   |           |
    | errors | bigint |           |


Execute the following error_rate view commands;

        CREATE VIEW error_rate AS
        SELECT total_table.date, round(100.0*error_table.errors/total_table.views,2) AS percentage
        FROM total_table, error_table
        WHERE total_table.date = error_table.date
        ORDER BY total_table.date;

To form error_rate table below;

    |   Column   |  Type   | Modifiers |
    |------------+---------+-----------|
    | date       | date    |           |
    | percentage | numeric |           |


#### Run queries:

    1. Press ctrl+z to exit
    2. Type the following command to execute queries;

       python logs.py
    

Line 13: Generate a text file (Source:http://www.pythonforbeginners.com/files/reading-and-writing-files-in-python)

Line 14 - 15: Execute PostgreSQL command in a database session(Source: https://www.a2hosting.com/kb/developer-corner/postgresql/connecting-to-postgresql-using-python)

Line 16: Write to text file (Source:https://www.a2hosting.com/kb/developer-corner/postgresql/connecting-to-postgresql-using-python)

Line 17: Read data from the database (Source: http://initd.org/psycopg/docs/cursor.html)

Line 22: Fetch all (remaining) rows of a query result, returning them as a list of tuples (Source: http://initd.org/psycopg/docs/cursor.html)

Python Style checked using http://pep8online.com/checkresult