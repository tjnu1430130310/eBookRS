# coding:utf-8
import sqlite3
from django.db import transaction

import jieba
import graphlab

# heck_same_thread 设置为 False，即可允许 sqlite 被多个线程同时访问
conn = sqlite3.connect('BookDB.sqlite3', check_same_thread=False)


# 评论的情感分析

def chinese_word_cut(mytext):
    return " ".join(jieba.cut(mytext))

@transaction.atomic
def make_sentimentmodel():
    
    with transaction.atomic():
        comments_data = graphlab.SFrame.from_sql(conn, "SELECT user_id, book_id, context, score_rating, created_time FROM books_comment")
    
    comments_data["content_cutted"] = comments_data["context"].apply(chinese_word_cut)
    comments_data['word_count'] = graphlab.text_analytics.count_words(comments_data["content_cutted"])
    good_data, bad_data = comments_data.dropna_split()

    # ignore all 3* reviews
    good_data = good_data[good_data['score_rating'] != 6]

    # positive sentiment = 4* or 5* reviews
    good_data['sentiment'] = good_data['score_rating'] > 6

    train_data, test_data = good_data.random_split(.8, seed=0)

    sentiment_model = graphlab.logistic_classifier.create(train_data, target='sentiment', features=['word_count'], validation_set=test_data)
    sentiment_model.save('helper/books_comments_sentiment_model')

    # comments_data['predicted_sentiment'] = sentiment_model.predict(comments_data, output_type='probability')
    # comments_data.sort('predicted_sentiment', ascending=False).save('helper/coeffi_comments_data')
    comments_data.save('helper/coeffi_comments_data')



# comments_data = graphlab.load_sframe('helper/coeffi_comments_data')
# sentiment_model = graphlab.load_model('helper/books_comments_sentiment_model')

@transaction.atomic
def comments_sentimenting(book_id):
    
    comments_data = graphlab.load_sframe('helper/coeffi_comments_data')
    sentiment_model = graphlab.load_model('helper/books_comments_sentiment_model')
    commentsFromABook = comments_data[comments_data['book_id'] == int(book_id)]
    commentsFromABook['predicted_sentiment'] = sentiment_model.predict(commentsFromABook, output_type='probability')
    # comments_data['predicted_sentiment'] = sentiment_model.predict(comments_data, output_type='probability')
    return commentsFromABook.sort('created_time', ascending=True)
    # return comments_data.sort('predicted_sentiment', ascending=ABool)


