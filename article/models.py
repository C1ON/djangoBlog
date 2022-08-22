from django.db import models
from ckeditor.fields import RichTextField


class Article(models.Model):
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE,
                               verbose_name="Yazar")  # on_delete, kullanıcıya ait olan tüm bilgileri siler.
    title = models.CharField(max_length=50, verbose_name="Başlık")
    content = RichTextField()
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturma Tarihi")  # O anki tarihi ekler.
    article_image = models.FileField(blank=True, null=True, verbose_name="Makaleye fotoğraf ekleyin")

    def __str__(self):
        return self.title


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="Makale", related_name="comments")
    comment_author = models.CharField(max_length=50, verbose_name="İsim")
    comment_content = models.CharField(max_length=200, verbose_name="Yorum")
    comment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment_content
