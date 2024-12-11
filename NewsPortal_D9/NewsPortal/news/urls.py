from django.urls import path
# Импортируем созданное нами представление
from .views import *


urlpatterns = [
   # path — означает путь.
   # В данном случае путь ко всем товарам у нас останется пустым,
   # чуть позже станет ясно почему.
   # Т.к. наше объявленное представление является классом,
   # а Django ожидает функцию, нам надо представить этот класс в виде view.
   # Для этого вызываем метод as_view.
   # pk — это первичный ключ товара, который будет выводиться у нас в шаблон
   # int — указывает на то, что принимаются только целочисленные значения

   path('', PostsList.as_view(), name='post_list'),
   path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
   path('search/', SearchPostsList.as_view(), name='search_post_list'),

   path('news/create/', PostCreate.as_view(), name='news_create'),
   path('articles/create/', PostCreate.as_view(), name='articles_create'),

   path('news/<int:pk>/update/', PostUpdate.as_view(), name='news_update'),
   path('articles/<int:pk>/update/', PostUpdate.as_view(), name='articles_update'),

   path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
   path('articles/<int:pk>/delete/', PostDelete.as_view(), name='articles_delete'),

   path('user_detail/<int:pk>/', UserDetail.as_view(), name='user_detail'),
   path('upgrade/', upgrade_me, name='upgrade'),

   path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),

]