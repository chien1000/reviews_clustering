from django.db import models
import datetime

# Create your models here.
class Movie(models.Model):

    movie_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=20)
    title_original = models.CharField(blank=True, max_length=50)
    director = models.CharField(max_length=20)
    cast = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    length = models.CharField(blank=True, max_length=100)
    date = models.DateField(default= datetime.date.min)
    review_count = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title


class Review(models.Model):

    movie = models.ForeignKey('Movie', related_name='reviews', on_delete=models.CASCADE)
    rate = models.IntegerField(default=0)
    date = models.DateField(default= datetime.date.min)
    author = models.CharField(blank=True, max_length=30)
    title = models.TextField(blank=True, default='')
    content = models.TextField(blank=True, default='')

    def __str__(self):
        return self.title

class Sentence(models.Model):

    review_id = models.ForeignKey('Review', related_name='sentences',on_delete=models.CASCADE)
    cluster_id = models.IntegerField(db_index=True,default=-1)
    review_position = models.IntegerField(null=True) #TODO: default value...
    content = models.TextField(blank=True, default='')
    cos_sim = models.FloatField(null=True, blank=True)
    jac_sim = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.content


class Tag(models.Model):

    movie = models.ForeignKey('Movie', related_name='tags',on_delete=models.CASCADE)
    name =  models.CharField(max_length=20)
    cluster_id = models.IntegerField(default=-1)
    
    def __str__(self):
        return self.name