from django.db import models
from django.conf import settings


class UserProfile(models.Model):
    """Perfil extendido del usuario."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tienda_profile'
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name='Teléfono')
    address = models.TextField(blank=True, verbose_name='Dirección')

    def __str__(self):
        return f'Perfil de {self.user.username}'


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Nombre')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio')
    stock = models.PositiveIntegerField(default=0, verbose_name='Stock')
    tags = models.ManyToManyField('Tag', blank=True, related_name='products')

    def __str__(self):
        return self.name


class Order(models.Model):
    """Pedido de un cliente."""

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pendiente'
        COMPLETED = 'completed', 'Completado'
        CANCELLED = 'cancelled', 'Cancelado'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, verbose_name='Cantidad')
    total = models.DecimalField(
        max_digits=10, decimal_places=2,
        default=0, verbose_name='Total'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Pedido #{self.pk} - {self.user.username}'


class ActivityLog(models.Model):
    """Registro de actividad (auditoría simple)."""
    description = models.TextField(verbose_name='Descripción')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'[{self.created_at:%Y-%m-%d %H:%M}] {self.description[:50]}'

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
# Create your models here.
