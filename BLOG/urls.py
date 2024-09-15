from django.urls import path
from . import views

urlpatterns = [
   path('blog/', views.blog_page, name='blog_page'),
   path('list_articles/', views.list_articles, name='list_articles'),
   path('article/<int:pk>/', views.article_detail, name='article_detail'),
   path('create_article', views.create_article, name='create_article'),
   path('update_article/<int:article_id>/', views.update_article, name='update_article'),
    path('delete_article/<int:article_id>/', views.delete_article, name='delete_article'),
]
