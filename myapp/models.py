from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime
from PIL import Image

# Create your models here.
# import pdb;pdb.set_trace()
User = get_user_model()

class Create_Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post_img = models.ImageField(upload_to='images')
    caption = models.CharField(max_length=350)
    date = models.DateTimeField(default=datetime.now()) 
    likes = models.ManyToManyField(User,related_name='likes',blank=True)
    news_likes_count = models.BigIntegerField(default='0')
    
    def __str__(self):
        return self.caption
    
    @property
    def total_likes(self):
        return self.likes.count()

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg',upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return f'{self.user.username} Profile'
    
    def save(self, *args, **kwargs):
        # save the profile first
        super().save(*args, **kwargs)

        # resize the image
        img = Image.open(self.image.path)
        if img.height > 150 or img.width > 150:
            output_size = (150, 150)
            # create a thumbnail
            img.thumbnail(output_size)
            
            # overwrite the large image
            img.save(self.image.path)


class Comment(models.Model):
  post = models.ForeignKey(Create_Post, on_delete=models.CASCADE, related_name='comments')
  name = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_by')
  body = models.TextField(help_text='Add a comment')
  date = models.DateTimeField(auto_now_add=True)