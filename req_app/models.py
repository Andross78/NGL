from django.db import models

# Create your models here.
class Author(models.Model):
    
    name = models.CharField(max_length=128, blank=True)
    aka = models.TextField(blank=True)
    api_key = models.CharField(max_length=10, blank=True, unique=True)
    views = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name


class Book(models.Model):

    title = models.CharField(max_length=128, blank=True)
    views = models.IntegerField(default=0)
    api_key = models.CharField(max_length=10, blank=True, unique=True)
    authors = models.ManyToManyField(Author, blank=True)

    def __str__(self):
        return self.title