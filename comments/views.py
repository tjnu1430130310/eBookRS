# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.utils.encoding import smart_text

from books.models import Book
from .models import Comment
from .forms import CommentForm


# Create your views here.

def book_comment(request, book_id):
    # 先获取被评论的文章，因为后面需要把评论和被评论的文章关联起来。
    # 使用Django 提供的一个快捷函数 get_object_or_404，其作用是当获取的电子书（Book）存在时，则获取；否则返回 404 页面给用户。
    book = get_object_or_404(Book, id=book_id)

    # HTTP 请求有 get 和 post 两种，一般用户通过表单提交数据都是通过 post 请求，因此只有当用户的请求为 post 时才需要处理表单数据。
    if request.method == 'POST':
        # 用户提交的数据存在 request.POST 中，这是一个类字典对象。
        # 我们利用这些数据构造了 CommentForm 的实例，这样 Django 的表单就生成了。
        form = CommentForm(request.POST)
        data = request.POST.copy()

        # 当调用 form.is_valid() 方法时，Django 自动帮我们检查表单的数据是否符合格式要求。
        if form.is_valid():
            # 检查到数据是合法的，

            # 调用表单的 save 方法保存数据到数据库，
            # commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库。
            comment = form.save(commit=False)

            # 将评论和被评论的文章关联起来。
            comment.book = book

            if request.user.is_authenticated():
                comment.user = request.user

            comment.read_count = 1

            comment.root_id = data.get('root_id', 0)
            comment.reply_to = data.get('reply_to', 0)
            comment.reply_name = data.get('reply_name', '')

            # 最终将评论数据保存进数据库，调用模型实例的 save 方法
            comment.save()

            # 重定向到 post 的详情页，实际上当 redirect 函数接收一个模型的实例时，它会调用这个模型实例的 get_absolute_url 方法，
            # 然后重定向到 get_absolute_url 方法返回的 URL。
            return redirect(book)
            # redirect 函数位于 django.shortcuts 模块中，它的作用是对 HTTP 请求进行重定向（即用户访问的是某个 URL，但由于某些原因，服务器会将用户重定向到另外的 URL）。
            # redirect 既可以接收一个 URL 作为参数，也可以接收一个模型的实例作为参数（例如这里的 post）。
            # 如果接收一个模型的实例，那么这个实例必须实现了 get_absolute_url 方法，这样 redirect 会根据 get_absolute_url 方法返回的 URL 值进行重定向。

        else:
            # 检查到数据不合法，重新渲染详情页，并且渲染表单的错误。
            # 因此我们传了三个模板变量给 detail.html，
            # 一个是电子书（Book），一个是评论列表，一个是表单 form
            # 注意这里我们用到了 post.comment_set.all() 方法，
            # 这个用法有点类似于 Post.objects.all()
            # 其作用是获取这篇 book 下的的全部评论，
            # 因为 Post 和 Comment 是 ForeignKey 关联的，
            # 因此使用 post.comment_set.all() 反向查询全部评论。
            comment_list = book.comment_set.all()
            context = {'book': book,
                       'form': form,
                       'comment_list': comment_list
                       }
            return render(request, 'bookTemp/detail.html', context=context)
    # 不是 post 请求，说明用户没有提交数据，重定向到文章详情页。
    return redirect(book)


# def get_queryset(self, context):
#     ctype, object_pk = self.get_target_ctype_pk(context)
#     if not object_pk:
#         return self.comment_model.objects.none()
#
#     # Explicit SITE_ID takes precedence over request. This is also how
#     # get_current_site operates.
#     # site_id = getattr(settings, "SITE_ID", None)
#     # if not site_id and ('request' in context):
#     #     site_id = get_current_site(context['request']).pk
#
#     qs = self.comment_model.objects.filter(
#         content_type=ctype,
#         # object_pk=smart_text(object_pk),
#         # site__pk=site_id,
#     )
#
#     # The is_public and is_removed fields are implementation details of the
#     # built-in comment model's spam filtering system, so they might not
#     # be present on a custom comment model subclass. If they exist, we
#     # should filter on them.
#     field_names = [f.name for f in self.comment_model._meta.fields]
#     if 'is_public' in field_names:
#         qs = qs.filter(is_public=True)
#     # if getattr(settings, 'COMMENTS_HIDE_REMOVED', True) and 'is_removed' in field_names:
#     #     qs = qs.filter(is_removed=False)
#     if 'user' in field_names:
#         qs = qs.select_related('user')
#
#     for q in qs:
#         q.replies = self.comment_model.objects.filter(
#             content_type=ctype,
#             object_pk=smart_text(object_pk),
#             # site__pk=settings.SITE_ID,
#             root_id=q.id,
#             is_public=True,
#             is_removed=False,
#         ).order_by('submit_date')
#
#     return qs
