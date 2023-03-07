from tokenize import blank_re
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from notifications.models import notify_handler
from notifications.signals import notify
from notifications.models import Notification


User = get_user_model()

# Create your models here.
class Tuman(models.Model):
    name = models.CharField(max_length=1000)
    
    class Meta:
        verbose_name = 'Tuman'
        verbose_name_plural = 'Tumanlar'

    def __str__(self):
        return f"Tuman object, {self.name}, id ({self.pk})"

class Mahalla(models.Model):
    name = models.CharField(max_length=1000)
    tuman = models.ForeignKey(Tuman, on_delete=models.CASCADE, related_name='mahalla')
    
    class Meta:
        verbose_name = 'Mahalla'
        verbose_name_plural = 'Mahallalar'

    def __str__(self):
        return f"Mahalla object, {self.name}, id ({self.pk})"


class RequestModel(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requests_as_sender')
    context = models.TextField(verbose_name="Text contexti")
    address = models.TextField()
    image = models.ImageField(upload_to='requests/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    hokimiyat_receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE, 
        related_name='requests_as_hokimiyat_receiver',
        null=True, 
        blank=True
    )
    kadastr_receiver = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='requests_as_kadastr_receiver',
        null=True, 
        blank=True,
    )
    qurilish_receiver = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='requests_as_qurilish_receiver',
        null=True, 
        blank=True,
    )

    class Meta:
        verbose_name = 'So\'rovnoma'
        verbose_name_plural = 'So\'rovnomalar'
        ordering = ['-created_at']
    
    def __str__(self) -> str:

        return f"So'rovnoma (id: {self.pk})"

    def clean(self) -> None:
        if self.hokimiyat_receiver == None and self.kadastr_receiver == None and self.qurilish_receiver == None:
            raise ValidationError("Kamida bitta qabul qiluvchi kiritilishi shart!")
        return super().clean()


class NotificationCTA(models.Model):
    notification = models.OneToOneField(Notification, on_delete=models.CASCADE)
    request_id = models.IntegerField(null=True, blank=True)


    def __str__(self):
        return str(self.request_id)

def custom_notify_handler(*args, **kwargs):
    notifications = notify_handler(*args, **kwargs)
    request_id = kwargs.get("request_id", "")
    for notification in notifications:
        NotificationCTA.objects.create(notification=notification, request_id=request_id)
    return notifications


notify.disconnect(notify_handler, dispatch_uid='notifications.models.notification')
notify.connect(custom_notify_handler)  # , dispatch_uid='notifications.models.notification')
