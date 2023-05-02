from tabnanny import verbose
from urllib import request, response
from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime, timezone, timedelta
from django.utils.safestring import mark_safe

User = get_user_model()



# Create your models here
class Response(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responses')
    buyruq = models.FileField(upload_to='buyruqlar/')
    extra_file = models.FileField(upload_to='qoshimchalar/', null=True, blank=True)
    request = models.ForeignKey(
        to='main.RequestModel', on_delete=models.CASCADE, related_name='responses', 
    )
    is_certified = models.BooleanField(
        default=False, 
        verbose_name="Qonuniymi",
    )
    created_at = models.DateTimeField(auto_created=True, auto_now_add=True)
    is_late = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Javob'
        verbose_name_plural = 'Javoblar'

    def __str__(self) -> str:
        return f"Javob, (id: {self.pk})"

    def clean(self) -> None:
        if hasattr(self, "request"):
            request_time = self.request.created_at
            if self.created_at:
                response_time = self.created_at
            else:
                response_time = datetime.now() - timedelta(hours=5)
                response_time = response_time.replace(tzinfo=timezone.utc)
            difference = response_time - request_time
            if difference.days > 5:
                self.is_late = True
            else:
                self.is_late = False
        # self.save()
        return super().clean()