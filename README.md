# eBookRS电子书推荐系统

基于B/S开发模式，在Django环境下，选择Python2.7结合SQLite3进行开发，使用机器学习包GraphLab Create进行数据处理，设计了一个电子书推荐系统，系统具有简单的个性化推荐功能

## 数据来源和模推荐型

系统用户数据、电子书数据及其部分评论、出版商数据来自豆瓣读书的电子图书。爬虫于2017年10月21日在第三方神箭手平台上部署启动，于2017年10月28日停止。由于神箭手平台的节点和时间限制，以及豆瓣收费电子书和免费电子书的xpath设置不一致，导致电子书数据有缺漏。

在豆瓣电子书中，其评论评分满分为5颗星，但是通过观察源代码发现，一颗星的分值应当为2，也就是说半星是1分，1星是2分，满分为10分。因此设置爬虫爬取电子书评论评分时选取的xpath为“//meta[@itemprop='ratingValue']/@content”。

将数据存入SQLite数据库，数据库中共存在18485本电子书信息，293343条电子书评论信息，10346位作者信息，461个出版商信息，117573位用户信息，从数据爬取到数据存入SQLite数据库的过程中，数据出现了折损。

系统使用机器学习包GraphLab Create建立基于项目相似性的推荐模型和基于流行度的推荐模型为用户做出电子书推荐。此外，系统还将使用随机电子书推荐作为补充。

同时，用户的打分可能并不与用户具体的情感相同，有时候评论中可能会参杂人类反讽的修辞，由此选择建立评论的情感分析模型，试着去理解那些好评和差评到底表达了什么。

## 系统运行界面

系统页面美化工具选择使用直观简洁的前端开发框架Bootstrap4。使用Sass修改了Bootstrap4的颜色主题。

![](https://github.com/tjnu1430130310/eBookRS/blob/master/static/img/running/127.0.0.1_8000_.png)

![](https://github.com/tjnu1430130310/eBookRS/blob/master/static/img/running/127.0.0.1_8000_user_index.png)

系统根据基于项目的协同过滤算法，为每一位用户实现基于项目相似性的电子书推荐，不同的用户个体，或者说不同的用户群体所接收到的电子书推荐意见并不完全相同，展现其个性化的一面。

![](https://github.com/tjnu1430130310/eBookRS/blob/master/static/img/running/127.0.0.1_8000_books_12578_.png)

![](https://github.com/tjnu1430130310/eBookRS/blob/master/static/img/running/%E6%83%85%E6%84%9F%E5%88%86%E6%9E%90%E7%95%8C%E9%9D%A2.gif)

使用默认的管理界面。

![](https://github.com/tjnu1430130310/eBookRS/blob/master/static/img/running/127.0.0.1_8000_admin_.png)
