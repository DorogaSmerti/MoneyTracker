from django.db import models

class Tasks(models.Model):
    title = models.CharField()
    completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} - {self.completed}'