from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.

class Genre(models.Model):
    genre = models.CharField(max_length=50)

class Question(models.Model):
    content = models.TextField()
    status = models.BooleanField(default=False)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    quser = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'quser')
    auser = models.ForeignKey(User, on_delete=models.CASCADE, related_name = 'auser')
    likecount = models.IntegerField()
    dislikecount = models.IntegerField()
    answer = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.answer

class Like(models.Model):
    like = models.BooleanField(default=False)
    lname = models.ForeignKey(User, on_delete=models.CASCADE)
    ques = models.ForeignKey(Question, on_delete=models.CASCADE)