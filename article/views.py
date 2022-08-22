from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse
from django.contrib import messages
from .forms import articleForm
from .models import Article, Comment
from django.contrib.auth.decorators import login_required


# Create your views here.

def articles(request):
    keyword = request.GET.get("keyword")
    if keyword:
        articles = Article.objects.filter(title__contains=keyword)
        return render(request, "articles.html", {"articles": articles})
    else:
        articles = Article.objects.all()

        return render(request, "articles.html", {"articles": articles})


def index(request):
    """    return HttpResponse("Anasayfa")  """
    return render(request, "index.html")


def about(request):
    return render(request, "about.html")


@login_required(login_url="user:login")
def dashboard(request):
    articles = Article.objects.filter(author=request.user)  # Sisteme hangi user girmiş ise onunkilerini alır

    context = {
        "articles": articles
    }

    return render(request, "dashboard.html", context)


@login_required(login_url="user:login")
def addArticle(request):
    form = articleForm(request.POST or None, request.FILES or None)  # Yüklenen dosyalara request.FILES'ta kalıyor.

    if form.is_valid():
        article = form.save(commit=False)  # Makale oluştururken user bilgisi verilmiyor.
        article.author = request.user  # Bu yüzden manuel olarak yapmamız gerekiyor
        article.save()

        messages.success(request, "Makale başarıyla oluşturuldu.")
        return redirect("article:dashboard")

    else:
        return render(request, "addarticle.html", {"form": form})


def detail(request, id):
    # article = Article.objects.filter(id=id).first() # İlk elemanı almak için first() kullanmak gerekir.
    article = get_object_or_404(Article, id=id)  # id=id olan Article classından objeyi al demektir.

    comments = article.comments.all()  # Article'a ait olan tüm commentleri alır.

    return render(request, "detail.html", {"article": article, "comments": comments})


@login_required(login_url="user:login")
def updateArticle(request, id):
    article = get_object_or_404(Article, id=id)
    form = articleForm(request.POST or None, request.FILES or None, instance=article)
    # instance=article parametre o anki article'ın bilgilerini getirir.

    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()

        messages.success(request, "Makale başarıyla güncellendi.")
        return redirect("article:dashboard")

    else:
        return render(request, "update.html", {"form": form})


@login_required(login_url="user:login")
def deleteArticle(request, id):
    article = get_object_or_404(Article, id=id)
    article.delete()
    messages.success(request, "Makale başarıyla silindi.")

    return redirect("article:dashboard")


def addComment(request, id):
    article = get_object_or_404(Article, id=id)

    if request.method == "POST":
        comment_author = request.POST.get("comment_author")
        comment_content = request.POST.get("comment_content")

        newComment = Comment(comment_author=comment_author, comment_content=comment_content)
        newComment.article = article

        newComment.save()

    messages.success(request, "Yorumunuz başarıyla gerçekleşti.")
    return redirect(reverse("article:detail", kwargs={"id": id}))
