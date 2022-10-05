from django.db import models

class Movie(models.Model):
    user_id = models.IntegerField()
    title = models.TextField()
    poster = models.TextField(blank=True, null=True)
    imdbid = models.TextField()
    year = models.TextField()

class Playlist(models.Model):
    user_id = models.IntegerField()
    public = models.BooleanField(default=False)