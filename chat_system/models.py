from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from app.models import consultation

# Create your models here.

class Chat(models.Model):
    created_time = models.DateTimeField(auto_now_add=True)
    consultation_id =  models.ForeignKey(consultation, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()

    def __unicode__(self):
        return self.message
