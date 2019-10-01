from datetime import datetime

from django.db import models

from apps.users.models import BaseModel
from apps.organizations.models import Teacher
from apps.organizations.models import CourseOrg
# 1.设计表结构有几个重要的点
"""
实体1 <关系> 实体2
课程 章节 视频 课程资源 
"""
# 2.实体的具体字段

# 3.每一个字段的类型，是否必填


class Course(BaseModel):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="teacher")
    course_org = models.ForeignKey(CourseOrg, null=True, blank=True, on_delete=models.CASCADE, verbose_name="course organization")
    name = models.CharField(verbose_name="course name", max_length=50)
    desc = models.CharField(verbose_name="course description", max_length=300)
    learn_times = models.IntegerField(default=0, verbose_name='learn_time(minutes)')
    degree = models.CharField(verbose_name='degree', choices=(('easy', 'easy'), ('medium', 'medium'), ('hard', 'hard')), max_length=8)
    students = models.IntegerField(default=0, verbose_name='number of students')
    fav_nums = models.IntegerField(default=0, verbose_name='like number')
    click_nums = models.IntegerField(default=0, verbose_name="click numberm")
    notice = models.CharField(verbose_name="notice", max_length=300, default="")
    category = models.CharField(default=u'backend', max_length=20, verbose_name='category of the course')
    tag = models.CharField(default='', verbose_name="course's tag", max_length=10)
    youneed_know = models.CharField(default='', max_length=300, verbose_name='what you need to know')
    teacher_tell = models.CharField(default='', max_length=300, verbose_name="teacher's advice")
    detail = models.TextField(verbose_name='detail of course')
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name="cover image", max_length=100)
    is_classics = models.BooleanField(default=False, verbose_name="if classic or not")
    is_banner = models.BooleanField(default=False, verbose_name="is banner or not")

    class Meta:
        verbose_name = 'course information'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def lesson_nums(self):
        return self.lesson_set.all().count()


class CourseTag(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="course")
    tag = models.CharField(max_length=100, verbose_name=u"course tag")

    class Meta:
        verbose_name = "course tag"
        verbose_name_plural = verbose_name


    def __str__(self):
        return self.tag


class Lesson(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)    #on_delete表示对应的外键数据被删除后，当前的数据应该怎么办
    name = models.CharField(max_length=100, verbose_name=u"lesson's name")
    learn_times = models.IntegerField(default=0, verbose_name=u"learn_time(minutes)")

    class Meta:
        verbose_name = "lesson"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Video(BaseModel):
    lesson = models.ForeignKey(Lesson, verbose_name="Lesson", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name=u"video name")
    learn_times = models.IntegerField(default=0, verbose_name=u"learn_times(minutes)")
    url = models.CharField(max_length=1000, verbose_name=u"url to visit")

    class Meta:
        verbose_name = "Video"
        verbose_name = verbose_name

    def __str__(self):
        return self.name


class CourseResource(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="course")
    name = models.CharField(max_length=100, verbose_name=u"name")
    file = models.FileField(upload_to="course/resourse/%y/%m", verbose_name="download address", max_length=200)

    class Meta:
        verbose_name = "course resource"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name