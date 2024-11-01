from django.views.generic import ListView, DetailView

from blog.models import Article
from blog.services import get_articles_from_cache


class ArticleListView(ListView):
    model = Article
    paginate_by = 6
    context_object_name = "articles_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Статьи блога"
        context["articles_list"] = get_articles_from_cache()
        return context


class ArticleDetailView(DetailView):
    model = Article

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views += 1
        self.object.save()
        return self.object
