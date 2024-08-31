# yabbyapp/models.py
from django.db import models

class Note(models.Model):
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='images/notes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
