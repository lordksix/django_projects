from django.urls import path, reverse_lazy
from . import views

app_name='ads'
urlpatterns = [
    path('', views.ArticleListView.as_view(), name='all'),
    path('ad/<int:pk>', views.ArticleDetailView.as_view(), name='article_detail'),
    path('ad/create', 
        views.ArticleCreateView.as_view(), name='article_create'),
    path('ad/<int:pk>/update', 
        views.ArticleUpdateView.as_view(), name='article_update'),
    path('ad/<int:pk>/delete', 
        views.ArticleDeleteView.as_view(), name='article_delete'),
    path('ad_picture/<int:pk>', views.stream_file, name='article_picture'),
    path('ad/<int:pk>/favorite',
    views.AddFavoriteView.as_view(), name='article_favorite'),
    path('ad/<int:pk>/unfavorite',
    views.DeleteFavoriteView.as_view(), name='article_unfavorite'),
]
