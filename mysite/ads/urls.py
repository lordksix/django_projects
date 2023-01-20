from django.urls import path, reverse_lazy
from . import views

app_name='ads'
urlpatterns = [
    path('', views.ArticleListView.as_view(), name='all'),
    path('article/<int:pk>', views.ArticleDetailView.as_view(), name='article_detail'),
    path('article/create', 
        views.ArticleCreateView.as_view(), name='article_create'),
    path('article/<int:pk>/update', 
        views.ArticleUpdateView.as_view(), name='article_update'),
    path('article/<int:pk>/delete', 
        views.ArticleDeleteView.as_view(), name='article_delete'),
    path('article_picture/<int:pk>', views.stream_file, name='article_picture'),
    path('article/<int:pk>/favorite',
    views.AddFavoriteView.as_view(), name='article_favorite'),
    path('article/<int:pk>/unfavorite',
    views.DeleteFavoriteView.as_view(), name='article_unfavorite'),
]
