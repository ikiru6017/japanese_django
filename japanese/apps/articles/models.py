import datetime
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from users.models import Profile
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


from django.utils import timezone
import datetime

class Article(models.Model):
    article_title = models.CharField('Название статьи', max_length = 200)
    pub_date = models. DateTimeField('Дата публикации')
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    content = RichTextUploadingField('Контент', config_name='default', blank=True, null=True)
    
    def __str__(self):
        return self.article_title

    def get_absolute_url(self):
        return reverse('articles:article-detail', kwargs={'pk': self.pk})
    
    def was_published_recently(self):
        return self.pub_date >= (timezone.now() - datetime.timedelta(days = 7))
    
    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = "Статьи"
    
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    comment_text = models.TextField('Текст комментария')
    comment_pub_date = models. DateTimeField('Дата комментария', default=timezone.now)
    
    def __str__(self):
        return self.author
    
    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = "Комментарии"