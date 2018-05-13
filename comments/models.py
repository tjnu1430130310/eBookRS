# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

# Create your models here.
# class Comment(models.Model):
#     username = models.CharField('用户名', max_length=100, blank=True)
#     email = models.EmailField('e-mail电子邮箱', max_length=255, blank=True)
#     url = models.URLField(blank=True)
#     context = models.TextField('评论内容')
#     created_time = models.DateTimeField('提交时间', auto_now_add=True)  # 为 DateTimeField 传递了一个 auto_now_add=True 的参数值
#     # auto_now_add 的作用是，当评论数据保存到数据库时，自动把 created_time 的值指定为当前时间
#     # created_time 记录用户发表评论的时间，我们肯定不希望用户在发表评论时还得自己手动填写评论发表时间，这个时间应该自动生成

#     # user = models.ForeignKey('books.User')
#     user = models.ForeignKey(settings.AUTH_USER_MODEL,
#                              verbose_name=_('user'),
#                              blank=True, null=True,
#                              # related_name="%(class)s_comments",
#                              on_delete=models.SET_NULL)
#     book = models.ForeignKey('books.Book', verbose_name='书籍')

#     score_rating_choices = (
#         ('1', '☆'),
#         ('2', '★'),
#         ('3', '★☆'),
#         ('4', '★★'),
#         ('5', '★★☆'),
#         ('6', '★★★'),
#         ('7', '★★★☆'),
#         ('8', '★★★★'),
#         ('9', '★★★★☆'),
#         ('10', '★★★★★'),
#     )
#     score_rating = models.IntegerField('评分', choices=score_rating_choices, blank=True, null=True)

#     # reply fields
#     root_id = models.IntegerField(default=0)
#     reply_to = models.IntegerField(default=0)
#     reply_name = models.CharField(max_length=50, blank=True)

#     # def __str__(self):  # On Python 3
#     def __unicode__(self):
#         return self.context[:20]

#     class Meta:
#         verbose_name = '评论'
#         verbose_name_plural = '评论'
