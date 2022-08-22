from django.contrib import admin
from .models import Article,Comment # (.models ) O anki klasöre git ve Article'ı import et.

admin.site.register(Comment)

@admin.register(Article) # Article modelini admin panelinde göstermeye yarar.
class ArticleAdmin(admin.ModelAdmin):

    list_display = ["title","author","created_date"]

    list_display_links = ["title","created_date"] # linklendirme

    search_fields = ["title"] # Arama.

    list_filter = ["created_date"] # Oluşturma tarihine göre filtreleme

    class Meta: #admin.ModelAdmin içindeki özellikleri kullanmamız için gerekli.
        model = Article
