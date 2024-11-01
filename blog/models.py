from django.db import models

BLANK_NULL_TRUE = {"blank": True, "null": True}


class Article(models.Model):
    """Blog article model"""

    title = models.CharField(max_length=250, verbose_name="Заголовок")
    summary = models.CharField(max_length=250, verbose_name="Краткое содержание")
    content = models.TextField(verbose_name="Текст статьи")
    preview = models.ImageField(
        upload_to="blog/", verbose_name="Изображение", **BLANK_NULL_TRUE
    )
    views = models.PositiveIntegerField(default=0, verbose_name="Просмотров")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_published = models.BooleanField(default=True, verbose_name="Публикация")

    def __str__(self):
        return f"{self.title} {self.content[:100]}"

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ("-created_at",)
