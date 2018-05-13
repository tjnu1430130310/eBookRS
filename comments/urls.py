# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views

app_name = 'comments'  # 给这个评论的 URL 模式规定命名空间
urlpatterns = [
    url(r'^comment/book/(?P<book_id>[0-9]+)/$', views.book_comment, name='book_comment'),
]