from django.db import models

from django.contrib.auth import get_user_model

from apps.users.models import BaseModel
from apps.courses.models import Course

UserProfile = get_user_model()

class Banner(BaseModel):
    title = models.CharField(max_length=100, verbose_name="title")
    image = models.ImageField(upload_to="banner/%Y/%m", max_length=200, verbose_name="image")
    url = models.URLField(max_length=200, verbose_name="visit address")
    index = models.IntegerField(default=0, verbose_name="index")

    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

class UserAsk(BaseModel):
    name = models.CharField(max_length=20, verbose_name="name")
    mobile = models.CharField(max_length=12, verbose_name="phone number")
    course_name = models.CharField(max_length=50, verbose_name=u"course name")

    class Meta:
        verbose_name = "user's questions"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{name}_{course}({mobile})".format(name=self.name, course=self.course_name, mobile=self.mobile)



class CourseComments(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="user")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="course")
    comments = models.CharField(max_length=200, verbose_name="content")

    class Meta:
        verbose_name = "course comments"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.comments



class UserFavorite(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="user")
    fav_id = models.IntegerField(verbose_name="favorite id")
    fav_type = models.IntegerField(choices=((1, "course"), (2, "organization"), (3, "teacher")), default=1, verbose_name="type")

    class Meta:
        verbose_name = "user's favorite"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{user}_{id}".format(user=self.user.username, id=self.fav_id)


class UserMessage(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="user")
    message = models.CharField(max_length=200, verbose_name="content")
    has_read = models.BooleanField(default=False, verbose_name="has read or not")

    class Meta:
        verbose_name = "user's message"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.message


class UserCourse(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="user")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="course")

    class Meta:
        verbose_name = "user's course"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.course.name