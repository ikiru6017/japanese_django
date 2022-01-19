from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Q

from ckeditor_uploader.fields import RichTextUploadingField

from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Article, Comment
from django.utils import timezone

def index(request):
    latest_articles_list = Article.objects.order_by('-pub_date')
    return render(request, 'articles/list.html', {'latest_articles_list': latest_articles_list})

class ArticleListView(ListView):
    model = Article
    template_name = 'articles/list.html'
    context_object_name = 'latest_articles_list'
    ordering = ['-pub_date']
    paginate_by = 5

class UserArticleListView(ListView):
    model = Article
    template_name = 'articles/user_articles.html'
    context_object_name = 'latest_articles_list'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Article.objects.filter(author=user).order_by('-pub_date')
    

class SearchResultView(ListView):
    model = Article
    template_name = 'articles/search_results.html'

    def get_queryset(self):     #Поиск по названию или автору статьи
        query = self.request.GET.get('q')
        if query:
            object_list = Article.objects.filter(Q(article_title__icontains=query) | Q(author_id__username__icontains=query))
            return object_list
        else:
            return Article.objects.all()

class ArticleDetailView(DetailView):
    model = Article
    

class ArticleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Article
    fields = ['article_title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        if self.request.user.profile.m_role == 'Administrator' or self.request.user.profile.m_role == 'Teacher':
            return True
        return False


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields = ['article_title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        article_gotten = self.get_object()
        if self.request.user == article_gotten.author or self.request.user.profile.m_role == 'Administrator':
            return True
        return False


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    success_url = '/'

    def test_func(self):
        article_gotten = self.get_object()
        if self.request.user == article_gotten.author or self.request.user.profile.m_role == 'Administrator':
            return True
        return False


def detail(request, article_id):
    try:
        article_gotten = Article.objects.get( id = article_id )
    except:
        raise Http404("Статья не найдена")
    
    latest_comments_list = article_gotten.comment_set.order_by('-id')        #Подгружаем комментарии
    
    return render(request, 'articles/article_detail.html', {'article': article_gotten, 'latest_comments_list':latest_comments_list})


def leave_comment(request, pk):
    try:
        article_gotten = Article.objects.get( id = pk )
    except:
        raise Http404("Статья не найдена")
        
    Comment.objects.create(article = article_gotten, author = request.user, comment_text = request.POST['text'], comment_pub_date = timezone.now())
    
    return HttpResponseRedirect( reverse('articles:article-detail', args= (article_gotten.id,)) )