# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

# from comments.models import Comment
# from helper.sentiment import make_sentimentmodel

from django.db import transaction

# @transaction.atomic
# class CommentAdmin(admin.ModelAdmin):
#     # list_display = ('first_name', 'last_name', 'email')  # list_display 项是一个字段名称的元组，用于列表显示，这些字段名称必须是模块中有的。
#     list_display = ('username', 'book', 'score_rating', 'context')
#     # # search_fields = ('first_name', 'last_name')  # 添加一个根据姓名查询的快速查询栏，大小写敏感，并且可以对两个字段进行检索。
#     # search_fields = ('username', )
#     list_display_links = ('context',)

#     readonly_fields = ('username', 'email', 'url', 'book', 'score_rating', 'context', 'created_time')  # 设置只读字段
#     fields = (('username', 'email'), ('book', 'score_rating', 'created_time'), 'context')

#     list_filter = ('created_time',)  # list_filter 字段元组创建过滤器，位于列表页面的右边。 Django 为日期型字段提供了快捷过滤方式，包含：今天、过往七天、当月和今年。这些是开发人员经常用到的

#     date_hierarchy = 'created_time'  # 使用 date_hierarchy 选项过滤日期的方式。修改好后，页面中的列表顶端会有一个逐层深入的导航条。
#     # date_hierarchy 接受的是 字符串 ，而不是元组。因为只能对一个日期型字段进行层次划分。

#     ordering = ('-created_time',)

#     actions_on_top = True
#     actions_on_bottom = True

#     actions = ['remake_sentimentmodel']
    
#     def remake_sentimentmodel(self, request, queryset):
#         try:
#             # queryset.update(status='p')

#             make_sentimentmodel()

#             self.message_user(request, "重建模型成功")
#         except:
#             self.message_user(request, "重建模型失败")
#     remake_sentimentmodel.short_description = "重新建立情感分析模型"

#     def has_add_permission(self, request):
#         # Should return True if adding an object is permitted, False otherwise.
#         # 如果允许添加对象，则返回 True，否则返回 False。
#         return False

# admin.site.register(Comment, CommentAdmin)