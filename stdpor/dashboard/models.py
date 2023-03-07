from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Notes(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    title=models.CharField(max_length=200)
    des=models.TextField()

    def __str__(self):
        return self.title
    
class Todo(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    is_finished = models.BooleanField(default=False)
    def __str__(self):
        return self.title

       