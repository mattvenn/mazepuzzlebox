from django.db import models

# Create your models here.
class Box(models.Model):
    pub_date = models.DateTimeField('date published')
    maze = models.CharField(max_length=400)
