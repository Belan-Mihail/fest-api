from django.db import models
from django.contrib.auth.models import User
from post.models import Post

# 44 serialezed
# 43 dont fogget make migrations

class Likes(models.Model):
    """
    Comment model, related to User and Post
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-created_at']
        # Sets of field names that, taken together, must be unique
        unique_together = ['owner', 'post']

    def __str__(self):
        return f'{self.owner} & {self.post}'
