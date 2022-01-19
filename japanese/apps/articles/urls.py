from django.urls import path
from .views import (
    ArticleListView,
    SearchResultView,
    ArticleDetailView,
    ArticleCreateView,
    ArticleUpdateView,
    ArticleDeleteView,
    UserArticleListView
)

from . import views

app_name = 'articles'
urlpatterns = [
    path('', ArticleListView.as_view(), name = 'index'),
    path('search/', SearchResultView.as_view(), name = 'search_results'),
    path('user/<str:username>', UserArticleListView.as_view(), name = 'user-articles'),
    path('<int:pk>/', ArticleDetailView.as_view(), name = 'article-detail'),
    path('new/', ArticleCreateView.as_view(), name = 'article-create'),
    path('<int:pk>/update', ArticleUpdateView.as_view(), name = 'article-update'),
    path('<int:pk>/delete', ArticleDeleteView.as_view(), name = 'article-delete'),
    path('<int:pk>/leave_comment/', views.leave_comment, name = 'leave_comment'),
]