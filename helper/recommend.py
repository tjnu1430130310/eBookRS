#coding:utf-8
import random

import graphlab
import sqlite3
from django.db import transaction

from books.models import Book

# heck_same_thread 设置为 False，即可允许 sqlite 被多个线程同时访问
conn = sqlite3.connect('BookDB.sqlite3', check_same_thread=False)  # conn = connection
with transaction.atomic():
    comments_data = graphlab.SFrame.from_sql(conn, "SELECT user_id, book_id, score_rating FROM books_comment")
    
train_data, test_data = comments_data.random_split(.8, seed=0)

def make_personalizedmodel():
    personalized_model = graphlab.item_similarity_recommender.create(train_data, user_id='user_id', item_id='book_id',  target='score_rating', similarity_type='cosine')
    personalized_model.save('helper/books_personalized_model')

def make_popularitymodel():
    popularity_model = graphlab.popularity_recommender.create(train_data, user_id='user_id', item_id='book_id')
    popularity_model.save('helper/books_popularity_model')

personalized_model = graphlab.load_model('helper/books_personalized_model')
popularity_model = graphlab.load_model('helper/books_popularity_model')
users = comments_data['user_id'].unique()

@transaction.atomic
def personalized_recommend(user_id):
    PR = personalized_model.recommend(users=[user_id], k=11)
    return PR['book_id']

@transaction.atomic
def similar_recommend(book_id):
    SR = personalized_model.get_similar_items([int(book_id)], k=11)
    return SR['similar']

    # (url.decode('utf-8')).encode('gb2312')

@transaction.atomic
def popularity_recommend():
    return popularity_model.recommend(users=[users[0]], k=11)


def rand_books(except_id=0):
    # 随机获取 10+1
    rand_count = 3

    # 先用 exclude 排除当前打开博文，exclude相当于“不等于”条件。
    # 再使用 order_by('?') 随机排序
    # 最后用切片器取前10条博客。
    return Book.objects.exclude(id=except_id).order_by('?')[:rand_count]
