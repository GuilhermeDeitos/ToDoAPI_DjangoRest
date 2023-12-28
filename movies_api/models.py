from django.db import models

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=300)
    release_year = models.IntegerField()
    timestamp = models.DateField(auto_now_add=True)
    genre = models.CharField(max_length=100)
    director = models.CharField(max_length=200)

    def __str__(self):
        return self.title
    



# Create your models here.
