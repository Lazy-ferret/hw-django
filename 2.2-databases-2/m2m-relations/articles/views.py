from django.shortcuts import render

from articles.models import Article


def articles_list(request):
    template = 'articles/news.html'
    # ordering = '-published_at'
    # object_list = Article.objects.all().order_by(ordering)
    object_list = Article.objects.all()
    context = {'object_list': object_list}

    return render(request, template, context)
