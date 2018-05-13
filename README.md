# eBookRS
电子书推荐系统

## 数据来源和模推荐型

本电子书推荐系统的用户数据、电子书数据及其部分评论、出版商数据来自豆瓣读书的电子图书。爬虫于2017年10月21日在第三方神箭手平台上部署，于2017年10月28日停止，共爬取到豆瓣电子书数据共有19765条。

系统使用机器学习包GraphLab Create建立基于项目相似性的推荐模型，模型使用基于项目的协同过滤算法，为用户做出个性化的电子书推荐。此外，系统还将建立基于流行度的推荐模型和使用随机推荐作为补充，为用户提供推荐服务。

同时，用户的打分可能并不与用户具体的情感相同，有时候评论中可能会参杂人类反讽的修辞，所以根据评论评分为标准的推荐不够准确，可能对推荐的电子书产生影响，需要对此进行排除，由此选择建立评论的情感分析模型，试着去理解那些好评和差评到底表达了什么。

## 系统运行界面

系统页面美化工具选择使用直观简洁的前端开发框架Bootstrap4。使用Sass修改了Bootstrap4的颜色主题。

![](https://github.com/tjnu1430130310/eBookRS/blob/master/static/img/running/127.0.0.1_8000_.png)

![](https://github.com/tjnu1430130310/eBookRS/blob/master/static/img/running/127.0.0.1_8000_user_index.png)

系统根据基于项目的协同过滤算法，为每一位用户实现基于项目相似性的电子书推荐，不同的用户个体，或者说不同的用户群体所接收到的电子书推荐意见并不完全相同，展现其个性化的一面。

![](https://github.com/tjnu1430130310/eBookRS/blob/master/static/img/running/127.0.0.1_8000_books_12578_.png)

![](https://github.com/tjnu1430130310/eBookRS/blob/master/static/img/running/%E6%83%85%E6%84%9F%E5%88%86%E6%9E%90%E7%95%8C%E9%9D%A2.gif)

使用默认的管理界面。

![](https://github.com/tjnu1430130310/eBookRS/blob/master/static/img/running/127.0.0.1_8000_admin_.png)
