from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from .models import Order, UserProfile, ActivityLog, Product
from django.db.models import F
from django.db.models.signals import post_delete
from django.db.models.signals import m2m_changed
from .models import Product, Tag
from django.dispatch import Signal

User = get_user_model()

order_completed = Signal()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Crea un perfil automáticamente cuando se registra un usuario."""
    if created:
        UserProfile.objects.create(user=instance)

@receiver(pre_save, sender=Order)
def calculate_order_total(sender, instance, **kwargs):
    """Calcula el total del pedido antes de guardarlo."""
    instance.total = instance.quantity * instance.product.price

@receiver(post_save, sender=Order)
def log_new_order(sender, instance, created, **kwargs):
    """Registra en el log cuando se crea un pedido nuevo."""
    if created:
        ActivityLog.objects.create(
            description=(
                f'Nuevo pedido #{instance.pk}: '
                f'{instance.quantity}x {instance.product.name} '
                f'por {instance.user.username} '
                f'(total: ${instance.total})'
            )
        )

@receiver(post_save, sender=Order)
def update_stock_on_order(sender, instance, created, **kwargs):
    """Descuenta stock del producto cuando se crea un pedido."""
    if created:
        Product.objects.filter(pk=instance.product_id).update(
            stock=F('stock') - instance.quantity
        )

@receiver(post_delete, sender=Order)
def restore_stock_on_delete(sender, instance, **kwargs):
    """Restaura el stock cuando se elimina un pedido."""
    Product.objects.filter(pk=instance.product_id).update(
        stock=F('stock') + instance.quantity
    )

@receiver(m2m_changed, sender=Product.tags.through)
def log_tags_changed(sender, instance, action, pk_set, **kwargs):
    """Registra cuando se agregan o quitan tags de un producto."""
    if action == 'post_add':
        tag_names = Tag.objects.filter(pk__in=pk_set).values_list('name', flat=True)
        ActivityLog.objects.create(
            description=f'Tags agregados a "{instance.name}": {", ".join(tag_names)}'
        )
    elif action == 'post_remove':
        tag_names = Tag.objects.filter(pk__in=pk_set).values_list('name', flat=True)
        ActivityLog.objects.create(
            description=f'Tags removidos de "{instance.name}": {", ".join(tag_names)}'
        )



# En tienda/signals.py

@receiver(order_completed)
def on_order_completed(sender, order, user, **kwargs):
    """Registra cuando un pedido se completa."""
    ActivityLog.objects.create(
        description=f'Pedido #{order.pk} completado por {user.username}'
    )


@receiver(order_completed)
def notify_stock_low(sender, order, user, **kwargs):
    """Alerta si el stock queda bajo después de completar pedido."""
    product = order.product
    product.refresh_from_db()
    if product.stock < 5:
        ActivityLog.objects.create(
            description=f'⚠ Stock bajo: {product.name} tiene solo {product.stock} unidades'
        )