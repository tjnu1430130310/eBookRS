# -*- coding: utf-8 -*-
from django.contrib import auth   # checks username and password handles login and log outs
from django.http import HttpResponseRedirect  # allows us to redirect the browser to a difference URL
from django.shortcuts import redirect, render
from django.template.context_processors import csrf  # csrf - cross site request forgery.

from django.contrib.auth.models import User
from books.models import Book

from helper import comments_count
from django.db import transaction
from django.utils.translation import ugettext as _, ugettext_lazy
from helper.recommend import personalized_recommend

import json

def login(request, extra_context=None):
    """
        Displays the login form for the given HttpRequest.
    """

    # username = request.POST.get('username', '')
    # password = request.POST.get('password', '')
    # user = auth.authenticate(username=username, password=password)
    # if user is not None and user.is_active:
    #     # Correct password, and the user is marked "active"
    #     auth.login(request, user)
    #     # Redirect to a success page.
    #     # return HttpResponseRedirect("/account/loggedin/")
    #     redirect('mainpage:index')
    # else:
    #     # Show an error page
    #     return HttpResponseRedirect("/account/invalid/")

    from django.contrib.auth.views import LoginView
    from accounts.forms import AccountsAuthenticationForm
    context = dict(
        # self.each_context(request),
        title=_('Log in'),
        app_path=request.get_full_path(),
        username=request.user.get_username(),
    )

    defaults = {
        'extra_context': context,
        'authentication_form': AccountsAuthenticationForm,
        # 'template_name': self.login_template or 'admin/login.html',
    }
    
    return LoginView.as_view(**defaults)(request)


def logout(request, extra_context=None):
    # auth.logout(request)
    # # Redirect to a success page.
    # # return HttpResponseRedirect("/account/loggedout/")
    # # return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    # c = {}
    # c.update(csrf(request))
    # return render(request, c)

    """
    Logs out the user for the given HttpRequest.

    This should *not* assume the user is already logged in.
    """
    from django.contrib.auth.views import LogoutView
    defaults = {
        'extra_context': dict(
            # self.each_context(request),
            # Since the user isn't logged out at this point, the value of
            # has_permission must be overridden.
            has_permission=False,
            **(extra_context or {})
        ),
    }

    return LogoutView.as_view(**defaults)(request)



#添加用户中心的响应方法
def user_index(request):
    '''show the user infomations'''
    data={}
    user = request.user
    #判断是否登录了
    if request.user.is_authenticated():
        # count_comments = comments_count.get_comments_count(user.id)
        # replies_count = comments_count.get_replies_count(user.id)
        # replyed_count = comments_count.get_to_reply_count(user.id)
        # last_talk_about = comments_count.last_talk_about(user.id)
        all_talk_about = comments_count.all_talk_about(user.id)

        time = []
        rating = []
        for item in list(all_talk_about):
            time.append(str(item.created_time))
            rating.append(item.score_rating)
        time = json.dumps(time)
        rating = json.dumps(rating)

        with transaction.atomic():
            personalizedRecommend = personalized_recommend(request.user.id)
            pRbooks = []
            for b in personalizedRecommend:
                pRbooks.append(Book.objects.filter(id=b).get())

        return render(request,'registration/user_index.html', locals())
    else:
        data['message'] = u'您尚未登录，请先登录' #提示消息
        data['goto_page'] = True #是否跳转
        data['goto_url'] = '/'  #跳转页面
        data['goto_time'] = 3000  #等待多久才跳转
        return render(request,'registration/message.html',data)