# coding:utf-8

from django.db import connection

import comments
from books.models import Book, Comment
# from comments.models import Comment


# 获取指定用户的评论数
# def get_comments_count(user_id, content_type='book'):
# #     """get the book comments count"""
#     return  Comment.objects.filter(user_id=user_id).count()


# 获取指定用户回复其他人的数量
# def get_replies_count(user_id, content_type='blog'):
#     """get the blog replies count"""
#     return Comment.objects.filter(user_id=user_id, root_id__gt=0).count()


# 获取指定用户被回复的次数
# def get_to_reply_count(user_id, content_type='blog'):
#     """get to be replyed count"""
    # 获得一个游标(cursor)对象
    # cursor = connection.cursor()
    # sql = ur"""select count(django_comments.id) from django_comments where user_id = %s and id in (select django_comments.reply_to from django_comments left join django_content_type on django_comments.content_type_id django_content_type.id where django_content_type.app_label = %s and root_id>0)"""
    # paras = [user_id, content_type]
    # cursor.execute(sql, paras)  # 执行sql语句
    # raw = cursor.fetchone()  # 获取第一行
    # return Comment.objects.filter(root_id__gt=0, reply_to__in=Comment.objects.filter(user_id=user_id)).count()
    # select count(comments_comment.id) from comments_comment where root_id > 0 and reply_to in (select comments_comment.id from comments_comment where user_id = 1)


# 获取最后一个参与评论或回复的电子书
# def last_talk_about(user_id, content_type='blog'):
#     """get last talk about blog"""
#     c = Comment.objects.filter(user_id=user_id).order_by('-created_time')

#     try:
#         return Book.objects.get(id=c[0].book_id)
#     except Exception as e:
#         return None


# 获取所有评论和回复
def all_talk_about(user_id):
    # """get all talk about blogs"""
    # sql = ur"""
    #     select blog_blog.* from blog_blog
    #     where id in (select django_comments.object_pk
    #     from django_comments
    #     left join django_content_type
    #     on django_comments.content_type_id = django_content_type.id
    #     where django_content_type.app_label = 'blog' and user_id=%s)
    #     """ % user_id
    #
    # blogs = list(Book.objects.raw(sql))  # raw_query对象是一个生成器
    # comment_model = comments.get_model()
    #
    # for blog in blogs:
    #     sql = ur"""
    #             select django_comments.*
    #             from django_comments
    #             left join django_content_type
    #             on django_comments.content_type_id = django_content_type.id
    #             where django_content_type.app_label = 'blog' and user_id=%s and django_comments.object_pk='%s'
    #             order by submit_date desc
    #         """ % (user_id, blog.id)
    #
    #     blog.comments = comment_model.objects.raw(sql)
    # return blogs

    return Comment.objects.only("book", "user").order_by("-created_time").filter(user_id=user_id)