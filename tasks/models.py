from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Task(models.Model):
    time_created = models.DateTimeField()
    deadline = models.DateTimeField()
    desciption = models.TextField()
    subject = models.CharField(max_length=128)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.subject
