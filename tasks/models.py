from django.db import models
from django.contrib.auth.models import User

class Tasks(models.Model):
    task_name=models.CharField(max_length=200)
    created_date=models.DateField(auto_now_add=True)
    status=models.BooleanField(default=False)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.task_name
