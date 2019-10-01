from datetime import datetime

from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

GENDER_CHOICES = (
    ('male', 'male'),
    ('female', 'female')
)

class BaseModel(models.Model):
    add_time = models.DateTimeField(default=datetime.now, verbose_name='add_time')
    # 防止生成表
    class Meta:
        abstract = True

class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50, verbose_name='Name', default='')
    birthday = models.DateField(verbose_name='Birthday', null=True, blank=True)
    gender = models.CharField(verbose_name='Gender', choices=GENDER_CHOICES, max_length=6)
    address = models.CharField(max_length=100, verbose_name='Address', default='')
    mobile = models.CharField(max_length=12, verbose_name='Mobile Phone Number')
    image = models.ImageField(upload_to='head_image/%Y/%m', default='head_image/default.jpg')

    class Meta:
        verbose_name = "User's information"
        verbose_name_plural = verbose_name


    # 使其在后端能有正常可读的显示
    def __str__(self):
        if self.nick_name:
            return self.nick_name
        else:
            return self.username
        return self.username