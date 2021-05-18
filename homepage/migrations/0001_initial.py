# Generated by Django 3.0.6 on 2020-06-26 13:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('status', models.BooleanField(default=False)),
                ('likecount', models.IntegerField()),
                ('dislikecount', models.IntegerField()),
                ('answer', models.TextField()),
                ('auser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='auser', to=settings.AUTH_USER_MODEL)),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homepage.Genre')),
                ('quser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField(default=False)),
                ('lname', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('ques', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homepage.Question')),
            ],
        ),
    ]
