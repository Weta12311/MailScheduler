from django.core.cache import cache

from blog.models import Article
from mailscheduler.settings import CACHE_ENABLED


def get_articles_from_cache():
    if not CACHE_ENABLED:
        return Article.objects.all()

    key = f"articles_list"
    articles = cache.get(key)

    if articles is None:
        articles = Article.objects.all()
        cache.set(key, articles)

    return articles
