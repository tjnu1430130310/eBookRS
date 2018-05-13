# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User


# Create your models here.
from django.urls import reverse


class Publisher(models.Model):
    name = models.CharField('出版商', max_length=30)

    # address = models.CharField(max_length=50)
    # city = models.CharField(max_length=60)
    # state_province = models.CharField(max_length=30)
    # country = models.CharField(max_length=50)
    # website = models.URLField()

    def __unicode__(self):
        # __unicode__() 方法告诉Python如何将对象以unicode的方式显示出来
        return self.name

    class Meta:
        # 在任意一个 model 类中使用 Meta 类，以设置一些与特定模型相关的选项
        ordering = ['name']
        # 如果设置了 ordering 选项，那么除非你检索时特意额外地使用了 order_by()，否则当你使用 Django 的数据库 API 去检索时，Publisher 对象的相关返回值默认地都会按 name 字段排序
        verbose_name = '出版商'
        verbose_name_plural = '出版商'


class Author(models.Model):
    # first_name = models.CharField(max_length=30)
    # last_name = models.CharField(max_length=40)
    name = models.CharField('作者', max_length=80)

    # 所有字段都默认 blank=False ，这使得它们不允许输入空值。当 blank=True ，作者的邮箱地址允许输入一个空值
    # email = models.EmailField(blank=True, verbose_name='e-mail')  # 参数名称 verbose_name 的显式使用， verbose_name='e-mail' 将 Author.email 的标签改为中间有个横线的 e-mail
    email = models.EmailField('e-mail电子邮箱', blank=True, null=True)  # 允许隐式使用参数名称 verbose_name

    # 但 ManyToManyField 和 ForeignKey 字段必须显式使用参数名称 verbose_name ，因为它们第一个参数必须是模块类

    def __unicode__(self):
        # return u'%s %s' % (self.first_name, self.last_name)
        return self.name

    class Meta:
        verbose_name = '作者'
        verbose_name_plural = '作者'


class Book(models.Model):
    title = models.CharField('书名', max_length=100)
    authors = models.ManyToManyField(Author, verbose_name='作者')
    url = models.TextField('地址', blank=True)

    image = models.ImageField('图片', upload_to='static/img/bookphoto/', blank=True, null=True)

    publisher = models.ForeignKey(Publisher, verbose_name='出版商', blank=True, null=True)
    publication_date = models.DateField('出版日期', blank=True, null=True)  # 把Book模块修改成允许 publication_date为空。

    # 如果想允许一个日期型（DateField、TimeField、DateTimeField）或数字型（IntegerField、DecimalField、FloatField）字段为空，需要使用 null=True 和 blank=True。
    # 添加 null=True 比添加 blank=True 复杂。添加 null=True 改变了数据的语义，即改变了CREATE TABLE语句，删除了publication_date字段上的 NOT NULL 。要完成这些改动，还需要更新数据库。

    def __unicode__(self):
        return self.title

        # 自定义 get_absolute_url 方法
        # 记得从 django.urls 中导入 reverse 函数

    def get_absolute_url(self):
        return reverse('detail', kwargs={'book_id': self.id})

    class Meta:
        verbose_name = '电子书'
        verbose_name_plural = '电子书'


#
# class User(models.Model):
#     name = models.CharField(max_length=100)
#     password = models.CharField(max_length=100, default='pbkdf2_sha256$36000$N75vqDyzE3Y7$4il1xh6yBImxojxaZ+NL4YETCZ6xOnn4qOarEQZULt4=')
#     email = models.EmailField(default='default@default.com')
#     # is_superuser = models.BooleanField(default=False)
#     # is_staff = models.BooleanField(default=False)
#     # is_active = models.BooleanField(default=True)
#
#     def __unicode__(self):
#         return self.name


class Comment(models.Model):
    # user = models.ForeignKey('books.User')
    user = models.ForeignKey(User,
                             blank=True, null=True,
                             # related_name="%(class)s_comments",
                             on_delete=models.SET_NULL)
    book = models.ForeignKey(Book, verbose_name='书籍')
    
    context = models.TextField('评论内容')
    
    score_rating = models.IntegerField('评分', blank=True, null=True)

    created_time = models.DateTimeField('提交时间', auto_now_add=True)  # 为 DateTimeField 传递了一个 auto_now_add=True 的参数值
    # auto_now_add 的作用是，当评论数据保存到数据库时，自动把 created_time 的值指定为当前时间
    # created_time 记录用户发表评论的时间，我们肯定不希望用户在发表评论时还得自己手动填写评论发表时间，这个时间应该自动生成

    # def __str__(self):  # On Python 3
    def __unicode__(self):
        return self.context[:20]

    class Meta:
        verbose_name = '豆瓣评论'
        verbose_name_plural = '豆瓣评论'
