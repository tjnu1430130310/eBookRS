# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

import django

from django import forms
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404, render_to_response

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.utils.encoding import smart_text
from django.views.decorators.csrf import csrf_protect, csrf_exempt, requires_csrf_token

import datetime

from books.models import Book, Author
from books.models import Comment as douban_Comment
# from comments.forms import CommentForm
# from comments.models import Comment
from helper.recommend import popularity_recommend, similar_recommend, rand_books, popularity_recommend
from helper.sentiment import comments_sentimenting

import json


def index(request):  # 不知道为什么，放这里会报错 Invalid index type: must be SArray, list, int, or str；2018年4月23日发现注释“from __future__ import unicode_literals”后，不再报错。。。人工智能是不可能智能的，你妹的智障！
    # post_list = Article.objects.all()  # 获取全部的Article对象
    # html = "<html><body>my homepage view." + "<a src='admin'>admin</a>" + "<a src='HelloView'>Hello View</a>" + "<a src='time'>time</a>" + "<a src='times/plus/'>times plus</a>" + "<a src='temp'>temp</a>" + "</body></html>"
    # return HttpResponse('index.html')
    popularity = popularity_recommend()
    pRbooks = []
    for i in range(len(popularity)):
        pRbooks.append(Book.objects.filter(id=popularity['book_id'][i]).get())

    return render_to_response('index.html', locals())



def display_meta(request):
    values = request.META.items()
    values.sort()
    # html = []
    # for k, v in values:
    #     html.append('<tr><td>%s</td><td>%s</td></tr>' % (k, v))
    # return HttpResponse('<table>%s</table>' % '\n'.join(html))
    return render_to_response('display_meta.html', {'values': values},)



# def search_form(request):
#     return render_to_response('search_form.html')


def search(request):
    # if 'q' in request.GET:
    #     message = 'You searched for: %r' % request.GET['q']
    #
    # if 'q' in request.GET and request.GET['q']:
    #     # 检查 q 是否存在于request.GET之外，还检查 reuqest.GET[‘q’] 的值是否为空
    #
    #     q = request.GET['q']
    #     books = Book.objects.filter(title__icontains=q)  # 获取数据库中标题包含q的书籍，不区分大小写。icontains 是一个查询关键字
    #     # 不推荐在一个包含大量产品的数据库中使用 icontains 查询，那会很慢
    #     # （在真实的案例中，可以使用以某种分类的自定义查询系统。 在网上搜索“开源 全文搜索”看看是否有好的方法）
    #
    #     return render_to_response('search.html',
    #                               {'books': books, 'query': q})
    #
    # else:
    #     # message = 'You submitted an empty form.'
    #     # return HttpResponse(message)
    #     # return HttpResponse('Please submit a search term.')
    #
    #     return render_to_response('search_form.html', {'error': True})  # 在检测到空字符串时，重新显示表单，并在表单上面给出错误提示以便用户立刻重新填写。
    #
    # # return HttpResponse(message)

    error = False
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:
            error = True
        else:
            # books = Book.objects.filter(title__icontains=q)
            books = Book.objects.filter( Q(authors__name__icontains=q) | Q(title__icontains=q) )
            return render_to_response('bookTemp/search.html', locals())
        return render_to_response('bookTemp/search.html', locals())

    # return render_to_response('search.html',
    #                           {'error': error},)
    return render_to_response('bookTemp/search.html', locals())


@transaction.atomic
def detail(request, book_id):
    # return HttpResponse("You're looking at book %s." % book_id)
    # request.user.id

    book = get_object_or_404(Book, id=book_id)

    # 获取这本 book 下的豆瓣评论
    with transaction.atomic():
        douban_comments = douban_Comment.objects.filter(book_id=book.id).order_by("-created_time")

    # 记得在顶部导入 CommentForm
    # form = CommentForm()
    # if request.user.is_authenticated():
    #     user = get_object_or_404(User, username=request.user.username)
    #     form.username = request.user.username
    #     form = CommentForm(instance=user)

    # 获取这本 book 下的全部评论
    # with transaction.atomic():
        # comments = Comment.objects.filter(book_id=book.id, root_id=0).order_by("-created_time")
        # for comment in comments:
        #     comment.replies = Comment.objects.filter(book_id=book.id, root_id=comment.id)

    # replies = Comment.objects.filter(book_id=book.id, root_id__gt=0)


    # 将文章、表单、以及文章下的评论列表作为模板变量传给 detail.html 模板，以便渲染相应数据。


    # recommend
    with transaction.atomic():
        similarRecommend = similar_recommend(book_id)
        sRbooks = []
        for b in similarRecommend:
            sRbooks.append(Book.objects.filter(id=b).get())

    randBooks = rand_books(book_id)

    # return render_to_response(request, 'bookTemp/detail.html', locals(), context_instance=RequestContext(request))  # error: render_to_response() got an unexpected keyword argument 'context_instance'
    return render(request, 'bookTemp/detail.html', locals())


@transaction.atomic
def comments_sentiment(request, book_id):
    commentsFromABook = comments_sentimenting(book_id)
    time = json.dumps(list(commentsFromABook['created_time']))
    sentiment = json.dumps(list(commentsFromABook['predicted_sentiment']))

    commentsFromABook = commentsFromABook.sort('predicted_sentiment', ascending=False)
    return render(request, 'bookTemp/comments_sentiment.html', locals())


def fulltext(request, book_id):
    return render(request, 'bookTemp/fulltext.html', locals())