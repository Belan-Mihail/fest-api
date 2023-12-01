from django.db import models
from django.contrib.auth.models import User

# 24 serialize/post
# 23 and add migration
class Post(models.Model):
    """
    Post model, related to 'owner', i.e. a User instance.
    Default image set so that we can always reference image.url.
    """
# 25
# first row for the database, second row of the tuple for display in the interface
# need to be above model fields
    image_filter_choices = [
            ('_1977', '1977'),
            ('brannan', 'Brannan'),
            ('earlybird', 'Earlybird'),
            ('hudson', 'Hudson'),
            ('inkwell', 'Inkwell'),
            ('lofi', 'Lo-Fi'),
            ('kelvin', 'Kelvin'),
            ('normal', 'Normal'),
            ('nashville', 'Nashville'),
            ('rise', 'Rise'),
            ('toaster', 'Toaster'),
            ('valencia', 'Valencia'),
            ('walden', 'Walden'),
            ('xpro2', 'X-pro II')
        ]
# 25-!

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    image = models.ImageField(
        upload_to='images/', default='../default_post_q4m4c4', blank=True
    )
    # 26 and make migrations
    image_filter = models.CharField(
        max_length=32, choices=image_filter_choices, default='normal'
    )
    # 26-!
    # 27 serializers


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.id} {self.title}'