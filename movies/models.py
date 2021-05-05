from django.db import models
from django.contrib.auth.models import User
import uuid


class Collections(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    movies = models.JSONField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
