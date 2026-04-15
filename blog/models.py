from django.db import models
from django.conf import settings


class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='Título')
    content = models.TextField(verbose_name='Contenido')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='articles',
        verbose_name='Autor'
    )
    published = models.BooleanField(default=False, verbose_name='Publicado')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Artículo'
        verbose_name_plural = 'Artículos'
        # Permisos personalizados (además de los 4 automáticos)
        permissions = [
            ('publish_article', 'Puede publicar artículos'),
            ('feature_article', 'Puede destacar artículos'),
        ]

    def __str__(self):
        return self.title