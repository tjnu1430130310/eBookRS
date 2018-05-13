# coding=utf-8
import random
import sqlite3
import time
import urllib2
from bs4 import BeautifulSoup

import os,django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Book.settings")# project_name 项目名称
django.setup()

from django.contrib.auth.models import User
# 伪造的头，不知到有用否
sendHeaders = {
    'User-Agent':'Mozilla/5.3 (Windows NT 7.2; rv:18.0) Gecko/20100101 Firefox/19.0',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Connection':'keep-alive'
}
# urlTmep = 'https://book.douban.com/top250?start='
urlTmep = 'https://read.douban.com/kind/1?start='
# print('正在保存第%d页的第%d条信息'%(i,k))
# saveFile = open('doubanAll2.txt','a')
# saveFile = open('douban.xlsx','a')

conn = sqlite3.connect('BookDB.sqlite3')
cur = conn.cursor()

# cur.execute()

# cur.execute("CREATE TABLE IF NOT EXISTS books_book (id INTEGER NOT NULL PRIMARY KEY autoincrement, title TEXT, publication_date date, publisher_id integer REFERENCES books_publisher(id) DEFERRABLE INITIALLY DEFERRED, url TEXT)")
# # OR IGNORE 子句表示如果有一个 INSERT 违反了“name必须唯一”的规则，那么数据库将忽略这个 INSERT 。数据库约束作为一个安全网络，确保不在无意中犯错
# cur.execute("CREATE TABLE IF NOT EXISTS books_author (id INTEGER NOT NULL PRIMARY KEY autoincrement, name TEXT UNIQUE)")
# cur.execute("CREATE TABLE IF NOT EXISTS books_publisher (id INTEGER NOT NULL PRIMARY KEY autoincrement, name TEXT UNIQUE)")
# cur.execute("CREATE TABLE IF NOT EXISTS books_book_authors (id INTEGER NOT NULL PRIMARY KEY autoincrement, book_id integer NOT NULL REFERENCES books_book(id) DEFERRABLE INITIALLY DEFERRED, author_id integer NOT NULL REFERENCES books_author(id) DEFERRABLE INITIALLY DEFERRED, UNIQUE (book_id, author_id))")
#
# cur.execute("CREATE TABLE IF NOT EXISTS books_user (id INTEGER NOT NULL PRIMARY KEY autoincrement, Name TEXT UNIQUE)")
# cur.execute("CREATE TABLE IF NOT EXISTS books_review (id INTEGER NOT NULL PRIMARY KEY autoincrement, book_id integer NOT NULL REFERENCES books_book(id) DEFERRABLE INITIALLY DEFERRED, user_id  integer NOT NULL REFERENCES books_user(id) DEFERRABLE INITIALLY DEFERRED, rating integer, context TEXT UNIQUE)")

conn.text_factory = str  ## !!!




def getBook(book_url):
    request = urllib2.Request(book_url, headers=sendHeaders)
    html = urllib2.urlopen(request)
    soup = BeautifulSoup(html, 'lxml')
    publish = soup.select('p[class=""]')[0].select('span[class="labeled-text"]')[0]  # print publish
    try :
        publisher_Name = publish.select('span:nth-of-type(1)')[0].text
        dtstr = publish.select('span:nth-of-type(2)')[0].text
        publication_date = sqlite3.datetime.datetime.strptime(dtstr, '%Y-%m').date()
    except:
        publisher_Name = None
        publication_date = None
    return (publisher_Name, publication_date)


def getReviews(book_id, book_url):
    for x in range(10):
        try:
            reviewsUrl = book_url + 'reviews?start=' + str(x * 25) + '&sort=score'  # print reviewsUrl
            request = urllib2.Request(reviewsUrl, headers=sendHeaders)

            reviewsHtml = urllib2.urlopen(request)
            reviewsSoup = BeautifulSoup(reviewsHtml, 'lxml')  # print reviewsSoup
            reviews = reviewsSoup.select('li[class="review-item collapsed col-media "]')  # print type(reviews)  # print len(reviews)

            for y in range(len(reviews)):
                user_Name = reviews[y].select('div[class="author"]')[0].text  # print user_Name
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
                    print 'No user, successfully insert' + str(user_id)

                rating = reviews[y].select('span')[0].get('title')  # print rating
                context = reviews[y].select('div[class="desc"]')[0].text  # print context
                reviewTime = reviews[y].select('meta[itemprop="datePublished"]')[0].get('content')  # print reviewTime

                # 存入 Reviews 表
                try:
                    cur.execute(
                        'INSERT OR IGNORE INTO books_review(book_id, user_id, rating, context, read_count, reviewTime) VALUES(?, ?, ?, ?, ?, datetime(?))',
                        (book_id, user_id, rating, context, 1, reviewTime))
                    review_id = cur.lastrowid
                    conn.commit()
                    print str(review_id) + ' is got'
                except:
                    print 'review get failed'
                # time.sleep(int(format(random.randint(0, 9))))  # 设置一个随机数时间，每爬一个网页可以随机的停一段时间，防止IP被封
        except:
            print 'URL error, review get failed: ' + reviewsUrl


start = time.clock()   # 设置一个时钟，这样我们就能知道我们爬取了多长时间了

k=1
# for i in range(11):
for i in range(100):
    url = urlTmep + str(i*20) + '&sort=hot&promotion_only=False&min_price=None&max_price=None&works_type=None'   # 页码是通过get方式获取，同每页在后面都是20的倍数，一共3页  # print url
    request = urllib2.Request(url, headers=sendHeaders)
    html=urllib2.urlopen(request)
    soup = BeautifulSoup(html,'lxml')
    book_title = soup.select('div[class="title"]')  # 找到名字所在的位置
    authorInfo = soup.select('span[class=""]')
    # booksInfo = soup.select('p[class="pl"]')  # 出版社相关所在的位置
    # ratingInfo = soup.select('span[class="rating_nums"]') # 评星所在的位置
    # commenInfo = soup.select('span[class="pl"]')   # 评价数量所在的位置
    # print(">>>>>>>>>>>>>>")
    for j in range(len(book_title)):
        print('正在保存第%d页的第%d条信息'%(i,k))
        # 每次使用select之后得到的是一个里列表，使用 attrs 必须在前面进行选择其中的元素来操作
        bookName = book_title[j].select('a')[0].text  # 获得书籍名

        cur.execute('SELECT id FROM books_book WHERE title = ? LIMIT 1', (bookName,))
        try:
            book_id = cur.fetchone()[0]
            print str(book_id) + ' got'

        except:
            book_url = 'https://read.douban.com' + book_title[j].select('a')[0].get('href')
            print bookName + ' is getting, url: ' + book_url
            authorName = authorInfo[j].select('a[class="author-item"]')[0].text  # 获得作者名

            # 获取书籍出版日期出版商评论
            (publisher_Name, publication_date) = getBook(book_url)  # print publisher_Name, publication_date

            # 存入数据库

            if publisher_Name is None:
                publisher_id = None
            else:
                # 插入 PublishersInfo 表
                cur.execute('SELECT id FROM books_publisher WHERE name = ? LIMIT 1', (publisher_Name, ))
                try:
                    publisher_id = cur.fetchone()[0]
                except:
                    cur.execute('INSERT OR IGNORE INTO books_publisher(Name) VALUES(?)', (publisher_Name, ))
                    publisher_id = cur.lastrowid  # print author_id
                    conn.commit()
                    print str(publisher_id) + ' is got'
                    if cur.rowcount != 1:
                        print 'No publisher account'
                conn.commit()
            # end if publisher_Name is None

            # 插入 BooksInfo 表
            cur.execute('INSERT OR IGNORE INTO books_book(title, url, publication_date, publisher_id) VALUES(?, ?, ?, ?)', (bookName, book_url, publication_date, publisher_id))
            book_id = cur.lastrowid  # print book_id

            # 插入 AuthorsInfo 表
            cur.execute('SELECT id FROM books_author WHERE name = ? LIMIT 1', (authorName, ))
            try:
                author_id = cur.fetchone()[0]
            except:
                cur.execute('INSERT OR IGNORE INTO books_author(name, email) VALUES(?, ?)', (authorName, None))
                author_id = cur.lastrowid  # print author_id
                conn.commit()
                print str(author_id) + ' is got'
                if cur.rowcount != 1:
                    print 'No author account'
            cur.execute('INSERT OR IGNORE INTO books_book_authors (book_id, author_id) VALUES(?, ?)', (book_id, author_id))
            conn.commit()

            # 获取评论
            getReviews(book_id, book_url)

        # end if book_id is not None

        k += 1

    time.sleep(int(format(random.randint(0, 9))))  # 设置一个随机数时间，每爬一个网页可以随机的停一段时间，防止IP被封
    # end for j in range(len(book_title))

# end for i in range(50)

end = time.clock()
print('Time Usage:', end - start)    #爬取结束，输出爬取时间
count = cur.execute('select * from books_book')
print('has %s record' % count)

cur.close()
conn.close()
# saveFile.close()

# # 抓取图书页方便测试
# tag3 = getHtml("http://book.douban.com/subject/25862578/?from=tag_all")
# file2 = open('web/book.html','wb')
# file2.write(tag3.encode())
# file2.close()
# print("成功")