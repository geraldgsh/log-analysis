#!/usr/bin/env python
# By geraldgsh
# Udacity Project 3: Log Analysis
#
# import Postgresql library
import psycopg2

DBNAME = "newsdata"


def popular_articles():
    # where 'w' writes to report.txt file
    g = open("report.txt", "w")
    db = psycopg2.connect("dbname=news")
    cur = db.cursor()
    g.write('Most popular articles:\n')
    # Find articles with number of views
    cur.execute("""SELECT title, count(path) as views
                FROM articles, log
                WHERE '/article/' || articles.slug = log.path
                GROUP BY title ORDER by views DESC LIMIT 3;""")
    results = cur.fetchall()
    print('\nThree most popular articles of all time;\n')
    for (title, views) in results:
        print("{} - {} views".format(title, views))
        g.write("{} - {} views\n".format(title, views))
    db.close()


def popular_authors():
    # where 'a' appends to report.txt file
    g = open("report.txt", "a")
    db = psycopg2.connect("dbname=news")
    cur = db.cursor()
    g.write('\nMost popular authors of all time;\n')
    # Find authors with number of articles views
    cur.execute("""SELECT n.name, v.views
                   FROM authors AS n
                   INNER JOIN viewer AS v ON v.author = n.id
                   GROUP BY n.name, v.views
                   ORDER BY v.views DESC;""")
    results = cur.fetchall()
    print('\nMost popular article authors of all time;\n')
    for (name, view) in results:
        print("{} - {} views".format(name, view))
        g.write("{} - {} views\n".format(name, view))
    db.close()


def error_status():
    # where 'a' appends to report.txt file
    g = open("report.txt", "a")
    db = psycopg2.connect("dbname=news")
    cur = db.cursor()
    g.write('\nDays with more than 1% errors:\n')
    # Form a table view of date and pageview
    # in relation with 404 NOT FOUND status
    cur.execute("""SELECT * FROM error_rate
                   WHERE error_rate.percentage > 1
                   ORDER BY error_rate.percentage DESC;""")
    results = cur.fetchall()
    print('\nDays with > 1% HTTP request errors are;\n')
    for (date, percentage) in results:
        print("{0:%d %B, %Y} - {1}% errors".format(date, percentage))
        g.write("{0:%d %B, %Y} - {1}% errors".format(date, percentage))
    db.close()


if __name__ == '__main__':
    popular_articles()
    popular_authors()
    error_status()

