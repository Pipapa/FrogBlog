import json
from flask import jsonify,url_for,request
from . import api
from .. import db
from ..models import User,Article,Category,Tag,Comment

# 不需要登录api 
@api.route('/api/article.list')
def get_articles():
    jsonObj = {'status':'False'}

    category = request.args.get('category')
    tag = request.args.get('tag')
    articles = []

    # 查询全部
    if category is None and tag is None:
        articles = Article.query.all()

    # 查询category
    if category is not None:
        category = Category.query.filter_by(name=category).first()
        if category is not None:
            articles = Article.query.filter_by(category_id=category.id).all()

    # 查询tag
    if tag is not None:
       articles = Article.query.filter(Article.tags.any(name=tag)).all()

    # 输出article
    if len(articles) != 0: 
        jsonObj['status']='OK'
        jsonObj['num_of_articles']=len(articles)
        for article in articles:
            info={}
            info['title']=article.title
            info['url']=url_for('user.articles_index',article_id=article.id)
            info['public_time']=article.public_time.strftime('%B %d %Y - %H:%M:%S')
            info['update_time']=article.update_time.strftime('%B %d %Y - %H:%M:%S')
            info['category']=article.get_category()
            info['tags']=article.get_tags()
            jsonObj[str(article.id)]=info
        return jsonify(jsonObj)

    return jsonify(jsonObj)

@api.route('/api/article.info')
def query_articles():
    # 查询id
    jsonObj = {'status':'False'}

    id = request.args.get('id')

    if id is not None:
        article = Article.query.get(id)
        if article is None:
            return jsonify(jsonObj)
        else:
            jsonObj['status'] = 'OK'
            content = {}
            content['title'] = article.title
            jsonObj['info']=article.get_info()
            return jsonify(jsonObj)
    return jsonify(jsonObj)