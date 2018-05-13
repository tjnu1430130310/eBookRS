# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.

from books.models import Publisher, Author, Book, Comment
from helper.recommend import make_personalizedmodel, make_popularitymodel
from helper.sentiment import make_sentimentmodel

# admin.site.register() 函数接受一个 ModelAdmin 子类作为第二个参数。如果忽略第二个参数，Django 将使用默认的选项。Publisher 的注册就属于这种情况。
admin.site.register(Publisher)  # 管理工具提供了一个放大镜图标方便你输入。点击那个图标将会弹出一个窗口，在那里你可以选择想要添加的 publisher

# admin.site.register(User)


class AuthorAdmin(admin.ModelAdmin):
    # AuthorAdmin 类是从 django.contrib.admin.ModelAdmin 派生出来的子类，保存着一个类的自定义配置，以供管理工具使用
    # list_display = ('first_name', 'last_name', 'email')  # list_display 项是一个字段名称的元组，用于列表显示，这些字段名称必须是模块中有的。
    list_display = ('name', 'email')
    # search_fields = ('first_name', 'last_name')  # 添加一个根据姓名查询的快速查询栏，大小写敏感，并且可以对两个字段进行检索。
    search_fields = ('name', )

# admin.site.register(Author)
admin.site.register(Author, AuthorAdmin)  # 用 AuthorAdmin 选项注册 Author 模块


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisher', 'publication_date')  # list_display 优化页面
    list_filter = ('publication_date',)  # list_filter 字段元组创建过滤器，位于列表页面的右边。 Django 为日期型字段提供了快捷过滤方式，包含：今天、过往七天、当月和今年。这些是开发人员经常用到的

    date_hierarchy = 'publication_date'  # 使用 date_hierarchy 选项过滤日期的方式。修改好后，页面中的列表顶端会有一个逐层深入的导航条。
    # date_hierarchy 接受的是 字符串 ，而不是元组。因为只能对一个日期型字段进行层次划分。

    ordering = ('-publication_date',)  # 改变默认的排序方式，使其按 publication date 降序排列。
    # ordering 选项基本像模块中 class Meta 的 ordering 那样工作，除了它只用列表中的第一个字段名。如果要实现降序，仅需在传入的列表或元组的字段前加上一个减号(-)
    # 列表页面默认按照模块 class Meta 中的 ordering 所指的列排序。但目前没有指定 ordering 值，所以当前排序是没有定义的

    # fields = ('title', 'authors', 'publisher', 'publication_date')  # 编辑表单将按照指定的顺序显示各字段
    # 默认地，表单中的字段顺序是与模块中定义一致。可以通过使用 ModelAdmin 子类中的 fields 选项来改变它
    fields = ('title', 'authors', 'image', 'publisher', 'publication_date', 'url')  # 可以隐藏publication_date，以防止它被编辑
    # 当一个用户用这个不包含完整信息的表单添加一本新书时，Django 会简单地将 publication_date 设置为 None，以确保这个字段满足 null=True 的条件
    readonly_fields = ('publication_date',)

    filter_horizontal = ('authors',)  # 针对多对多字段进行自定义，生成一个精巧的 JavaScript 过滤器
    # 针对那些拥有十个以上选项的多对多字段，建议使用 filter_horizontal
    # ModelAdmin 类还支持 filter_vertical 选项。 它像 filter_horizontal 那样工作，除了控件都是垂直排列，而不是水平排列的。 至于使用哪个，只是个人喜好问题。

    raw_id_fields = ('publisher',)
    search_fields = ('title',)

# admin.site.register(Book)
admin.site.register(Book, BookAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'context', 'score_rating', 'created_time')
    readonly_fields = ('user', 'book', 'context', 'score_rating', 'created_time')

    # 指定用于链接修改页面的字段
    list_display_links = ('context',)

    def has_add_permission(self, request):
        # Should return True if adding an object is permitted, False otherwise.
        # 如果允许添加对象，则返回 True，否则返回 False。
        return False
    
    actions_on_top = True
    actions_on_bottom = True
    actions = ['remake_personalizedmodel', 'remake_popularitymodel', 'remake_sentimentmodel']
    
    def remake_personalizedmodel(self, request, queryset):
        try:
            make_personalizedmodel()
            self.message_user(request, "重建模型成功")
        except:
            self.message_user(request, "重建模型失败")
    remake_personalizedmodel.short_description = "重新建立基于项目相似度的个性化推荐模型"

    def remake_popularitymodel(self, request, queryset):
        try:
            make_popularitymodel()
            self.message_user(request, "重建模型成功")
        except:
            self.message_user(request, "重建模型失败")
    remake_popularitymodel.short_description = "重新建立基于流行度的推荐模型"

    def remake_sentimentmodel(self, request, queryset):
        try:
            # queryset.update(status='p')
            make_sentimentmodel()
            self.message_user(request, "重建模型成功，报告已生成")
        except:
            self.message_user(request, "重建模型失败")
    remake_sentimentmodel.short_description = "重新建立情感分析模型"

admin.site.register(Comment, CommentAdmin)