from django.db import models
from django.conf import settings


def user_profile_path(instance, filename):
    """Guarda la foto en media/profile_pics/user_<id>/<filename>"""
    return f'profile_pics/user_{instance.user.id}/{filename}'


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    avatar = models.ImageField(
        upload_to=user_profile_path,
        blank=True,
        null=True,
        verbose_name='Foto de perfil'
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='Biografía'
    )
    birth_date = models.DateField(
        blank=True,
        null=True,
        verbose_name='Fecha de nacimiento'
    )

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'

    def __str__(self):
        return f'Perfil de {self.user.username}'
# Create your models here.
