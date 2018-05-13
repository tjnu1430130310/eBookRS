# eBookRS
电子书推荐系统

系统使用机器学习包GraphLab Create建立基于项目相似性的推荐模型，模型使用基于项目的协同过滤算法，为用户做出个性化的电子书推荐。此外，系统还将建立基于流行度的推荐模型和使用随机推荐作为补充，为用户提供推荐服务。
同时，用户的打分可能并不与用户具体的情感相同，有时候评论中可能会参杂人类反讽的修辞，所以根据评论评分为标准的推荐不够准确，可能对推荐的电子书产生影响，需要对此进行排除，由此选择建立评论的情感分析模型，试着去理解那些好评和差评到底表达了什么。

## 系统运行界面
![](https://github.com/tjnu1430130310/eBookRS/blob/master/static/img/running/127.0.0.1_8000_.png)