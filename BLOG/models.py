from django.db import models
from system_management.models import User

# Create your models here.
class BlogArticle(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    file = models.ImageField(upload_to='blog_files/', blank=True, null=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    article = models.ForeignKey(BlogArticle, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.article}'