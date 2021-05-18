from django.contrib import admin
from .models import Question, Genre, Like

# Register your models here.
admin.site.register(Question)
admin.site.register(Genre)
admin.site.register(Like)