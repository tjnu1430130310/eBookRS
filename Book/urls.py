"""Book URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import django
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
# from django.contrib.auth.views import login, logout
from accounts.views import login, logout

from accounts.views import user_index
from books import views as booksViews
from contact import views as ContactViews
from Home import HelloView

# from Book.Home.HelloView import hello, my_homepage_view, current_datetime, hours_ahead
# from Book.Home.temp import temp
# from books import views
# from contact.views import contact
# urlpatterns = [
#     url(r'^$', my_homepage_view),
#     url(r'^admin/', admin.site.urls),
#     url(r'^HelloView/', hello),
#     url(r'^time/', current_datetime),
#     url(r'^times/plus/(\d{1,2})/$', hours_ahead),
#     url(r'^temp', temp),
#     url(r'^search/$', views.search),
#     url(r'^display_meta/', views.display_meta),
#     url(r'^contact/', contact),
# ]
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', booksViews.index, name="index"),
    url(r'^HelloView/', HelloView.hello),
    url(r'^time/', HelloView.current_datetime, name="time"),
    url(r'^times/plus/(\d{1,2})/$', HelloView.hours_ahead),
    url(r'^display_meta/', booksViews.display_meta),
    url(r'^search/$', booksViews.search, name="search"),
    url(r'^books/(?P<book_id>[0-9]+)/$', booksViews.detail, name='detail'),
    url(r'^fulltext/(?P<book_id>[0-9]+)/$', booksViews.fulltext),
    url(r'^sentiment_comments/(?P<book_id>[0-9]+)/$', booksViews.comments_sentiment, name='sentiment'),
    # url(r'', include('comments.urls')),
    url(r'^contact/', ContactViews.contact),
    url(r'^accounts/login/$', login, name="login"),
    # url(r'^accounts/login/$', django.contrib.auth.views.login),
    url(r'^accounts/logout/$', logout, name="logout"),
    # url(r'^accounts/register/$', booksViews.register, name='register'),
    url(r'^user_index$', user_index, name='user_index')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
