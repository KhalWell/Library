from django.db.models.signals import post_save, pre_save
from core.models import Order
from core.tasks import upload_m2m_model


def update_books_status(sender, instance, *args, **kwargs) -> None:
    if instance.to_change:
        upload_m2m_model.apply_async(kwargs={'payload': instance.pk}, countdown=5)
    else:
        pass


def change_books(sender, instance: Order, **kwargs):
    if instance.pk is None:
        instance.to_change = True
    else:
        previous = Order.objects.get(pk=instance.pk)
        if previous.status != instance.status or previous.reserved != instance.reserved:  # field will be updated
            instance.to_change = True


post_save.connect(update_books_status, sender=Order)
pre_save.connect(change_books, sender=Order)
