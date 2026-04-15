from django.urls import path
from . import views

urlpatterns = [
    path('articles/', views.article_list, name='article_list'),
    path('articles/new/', views.article_create, name='article_create'),
    path('articles/<int:pk>/delete/', views.article_delete, name='article_delete'),
    path('articles/<int:pk>/publish/', views.article_publish, name='article_publish'),
    path('articles/<int:pk>/edit/', views.article_edit, name='article_edit'),
]