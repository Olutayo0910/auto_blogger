from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BlogPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    youtube_title = models.CharField(max_length=300)
    generated_content = models.TextField()
    youtube_link = models.URLField(default='https://www.youtube.com/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.youtube_title
