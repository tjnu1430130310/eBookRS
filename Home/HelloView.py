# -*- coding: utf-8 -*-
from django.conf import settings
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response, render, redirect

import datetime

from books.models import Book
from helper.recommend import popularity_recommend


def current_datetime(request):
    #now = datetime.datetime.now()

    #html = "<html><body>It is now %s.</body></html>" % now

    # t = Template("<html><body>It is now {{ current_date }}.</body></html>")
    # html = t.render(Context({'current_date': now}))

    # Simple way of using templates from the filesystem.
    # This is BAD because it doesn't account for missing files!

    # fp = open('templates/temp.html')
    # t = Template(fp.read())
    # fp.close()

    #t = get_template('current_datetime.html')

    #c = Context({'current_date': now})

    #html = t.render(c)

    #return HttpResponse(html)
    #return render_to_response('current_datetime.html', {'current_date': now})
    current_date = datetime.datetime.now()
    return render_to_response('current_datetime.html', locals())

def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()

    # dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    # html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    # return HttpResponse(html)

    hour_offset = offset
    next_time = datetime.datetime.now() + datetime.timedelta(hours=offset)
    return render_to_response('hours_ahead.html', locals())



def hello(request):
    return HttpResponse("Hello world")


def index(request):
    # post_list = Article.objects.all()  # 获取全部的Article对象
    # html = "<html><body>my homepage view." + "<a src='admin'>admin</a>" + "<a src='HelloView'>Hello View</a>" + "<a src='time'>time</a>" + "<a src='times/plus/'>times plus</a>" + "<a src='temp'>temp</a>" + "</body></html>"
    # return HttpResponse('index.html')
    popularity = popularity_recommend()
    p = popularity['book_id']
    pRbooks = []
    for i in range(len(popularity)):
        pRbooks.append(Book.objects.filter(id=popularity['book_id'][i]).get())

    return render_to_response('index.html', locals())