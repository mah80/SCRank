from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)    
    name = models.CharField(max_length=500,default="")
    result =  models.FileField(upload_to='results/')
    created_at = models.DateTimeField(("Created at"),auto_now_add=True, null=True)
    updated_at = models.DateTimeField(("Updated at"),auto_now=True)
    def __str__(self):
        return f"{self.updated_at}"
