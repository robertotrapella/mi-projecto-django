# En una vista o servicio:
from tienda.signals import order_completed


def complete_order(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    order.status = Order.Status.COMPLETED
    order.save()

    # Disparar signal personalizado
    order_completed.send(
        sender=Order,
        order=order,
        user=request.user
    )
# Create your views here.
