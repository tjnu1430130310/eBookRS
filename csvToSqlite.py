# coding=utf-8
import json
import sys
import csv

# csv.field_size_limit(sys.maxsize)
# On Windows 8.1 64bit with Python 2.6, maxInt = sys.maxsize returns 9223372036854775807L which consequently results in a TypeError: limit must be an integer
# when calling csv.field_size_limit(maxInt). Interestingly, using maxInt = int(sys.maxsize) does not change this.
import traceback

csv.field_size_limit(2147483647)
# A crude workaround is to simlpy use csv.field_size_limit(2147483647) which of course cause issues on other platforms.
# In my case this was adquat to identify the broken value in the CSV, fix the export options in the other application and remove the need for csv.field_size_limit()

import sqlite3

import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Book.settings")  # project_name 项目名称
django.setup()
from django.contrib.auth.models import User


# return publisher_id
def getPublish(publisher_Name):
    try:
        # publisher_Name = row['出版商(books_book.publisher)']
        if publisher_Name == '':
            publisher_id = None
        else:
            # 插入 PublishersInfo 表

            # 检测是否存在出版商
            cur.execute('SELECT id FROM books_publisher WHERE name = ? LIMIT 1', (publisher_Name,))
            try:
                # 有出版社，得到出版商id
                publisher_id = cur.fetchone()[0]
            except:
                # 无出版商，插入 PublishersInfo 表
                cur.execute('INSERT OR IGNORE INTO books_publisher(Name) VALUES(?)', (publisher_Name,))
                publisher_id = cur.lastrowid  # print author_id
                conn.commit()
                print str(publisher_id) + ' is got'
                if cur.rowcount != 1:
                    print '新增出版商失败'
            conn.commit()
        # end if publisher_Name == ''
        return publisher_id
    except:
        print 'getPubliser出错'


# return book_id
def getBook(row):
    try:
        bookName = row['书名(books_book.title)']
        try:
            cur.execute('SELECT id FROM books_book WHERE title = ? LIMIT 1', (bookName,))
            book_id = cur.fetchone()[0]
            print 'book ' + str(book_id) + '已存在'
        except:
            dtstr = row['出版日期(books_book.publication_date)']
            if dtstr == '':
                publication_date = None
            else:
                publication_date = sqlite3.datetime.datetime.strptime(dtstr, '%Y-%m').date()

            # publisher_Name = row['出版商(books_book.publisher)']
            publisher_id = getPublish(row['出版商(books_book.publisher)'])
            book_url = row['爬取链接(__url)']
            cur.execute(
                'INSERT OR IGNORE INTO books_book(title, url, publication_date, publisher_id) VALUES(?, ?, ?, ?)',
                (bookName, book_url, publication_date, publisher_id))
            book_id = cur.lastrowid  # print book_id
            conn.commit()

        return book_id
    except:
        print 'getBook出错'


# return author_id
def getAuthor(row):
    try:
        authorName = row['作者(books_book.author)']
        cur.execute('SELECT id FROM books_author WHERE name = ? LIMIT 1', (authorName,))
        try:
            author_id = cur.fetchone()[0]
        except:
            cur.execute('INSERT OR IGNORE INTO books_author(name, email) VALUES(?, ?)', (authorName, None))
            author_id = cur.lastrowid  # print author_id
            conn.commit()
            print 'author' + str(author_id) + ' 成功获取'
            if cur.rowcount != 1:
                print '新增作者失败'
        return author_id
    except:
        print 'getAuthor出错'


def getbooks_books_authors(book_id, author_id):
    cur.execute('SELECT id FROM books_book_authors WHERE book_id = ? AND author_id = ? LIMIT 1', (book_id, author_id))
    try:
        record_id = cur.fetchone()[0]
        print '书与作者关系记录 ' + str(record_id) + ' is got'
    except:
        cur.execute('INSERT OR IGNORE INTO books_book_authors (book_id, author_id) VALUES(?, ?)', (book_id, author_id))
        record_id = cur.lastrowid
        conn.commit()
        print 'books_books_authors ' + str(record_id) + ' 插入成功'


# return user_id
def getUser(jsondata):
    try:
        user_Name = jsondata['username'][0]  # print user_Name
        # 存入数据库

        # 存入 Users 表
        # cur.execute('SELECT id FROM books_user WHERE name = ? LIMIT 1', (user_Name,))
        cur.execute('SELECT id FROM auth_user WHERE username = ? LIMIT 1', (user_Name,))
        try:
            user_id = cur.fetchone()[0]
        except:
            # cur.execute('INSERT OR IGNORE INTO books_user(name) VALUES(?)', (user_Name,))
            # user_id = cur.lastrowid
            # conn.commit()
            # print 'No user, insert' + str(user_id)

            u = User.objects.create(username=user_Name)
            user_id = u.id
            print 'No user, successfully insert User' + str(user_id)

        return user_id
    except Exception, e:
        print 'getUser出错' + str(Exception)
        print 'traceback.print_exc():'; traceback.print_exc()
        print 'traceback.format_exc():\n%s' % traceback.format_exc()

        # IF OUT : IntegrityError: UNIQUE constraint failed: auth_user.username
        # up vote 3 down vote I finally figured out the causes and list them here. This can help someone who run into the same situation as me.
        # SITE_ID in settings.py shall be changed to match the site_id in admin Add the signup in the custom sign up form. Please see here How to customize user profile when using django-allauth


def getComment(jsondata, book_id, user_id):
    try:
        # user_id = getUser(jsondata)
        username = jsondata['username'][0]
        context = jsondata['comments_content'][0]

        try:
            cur.execute('SELECT id FROM comments_comment WHERE book_id = ? AND user_id = ? AND context = ? LIMIT 1',
                        (book_id, user_id, context))
            record_id = cur.fetchone()[0]
            print '评论记录 ' + str(record_id) + ' 已经存在，跳过插入'
        except:

            dtstr = jsondata['created_time'][0]
            created_time = sqlite3.datetime.datetime.strptime(dtstr, '%Y-%m-%d %H:%M:%S')  # print reviewTime

            score_rating = int(jsondata['score_rating'][0])
            # 存入 comments_comment 表
            try:
                cur.execute(
                    'INSERT OR IGNORE INTO comments_comment(username, email, url, context, created_time, score_rating, root_id, reply_to, reply_name, book_id, user_id) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                    (username, '', '', context, created_time, score_rating, 0, 0, '', book_id, user_id))
                review_id = cur.lastrowid
                conn.commit()
                print 'comment ' + str(review_id) + ' is got'
            except:
                print 'comment get failed'
    except:
        print 'getComments出错'


def getReadCount(book_id, user_id):
    try:
        try:
            cur.execute('SELECT id FROM books_readcount WHERE book_id = ? AND user_id = ? LIMIT 1', (book_id, user_id))
            record_id = cur.fetchone()[0]
            print '阅读记录 ' + str(record_id) + ' is got'
        except:
            cur.execute(
                'INSERT INTO books_readcount(book_id, user_id, read_count) VALUES(?, ?, ?)', (book_id, user_id, 1))
            record_id = cur.lastrowid
            conn.commit()
            print 'ReadCount ' + str(record_id) + '成功获取'
    except Exception, e:
        print 'getReadCount出错' + str(Exception)
        print 'traceback.print_exc():'; traceback.print_exc()
        print 'traceback.format_exc():\n%s' % traceback.format_exc()


# 将JSON格式的数据中的 /n 替换 为 <br />
def JsonFilter(jsonstr):
    jsonstr = jsonstr.replace("\n", "<br />")
    return jsonstr


conn = sqlite3.connect('BookDB.sqlite3')
cur = conn.cursor()

with open('crawler-data-794637-1508719512901.csv', 'rb') as f:
    reader = csv.DictReader(f)
    for row in reader:
        print row
        book_id = getBook(row)
        author_id = getAuthor(row)
        getbooks_books_authors(book_id, author_id)

        comments_data = JsonFilter(row['评论(comments)'])
        comments_json = json.loads(comments_data)
        for comment_json in comments_json:
            user_id = getUser(comment_json)
            getComment(comment_json, book_id, user_id)
            getReadCount(book_id, user_id)

cur.close()
conn.close()
