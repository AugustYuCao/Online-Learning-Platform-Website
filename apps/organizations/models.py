from django.db import models

from apps.users.models import BaseModel

class City(BaseModel):
    name = models.CharField(max_length=20, verbose_name=u"city")
    desc = models.CharField(max_length=200, verbose_name=u"description")

    class Meta:
        verbose_name = "city"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class CourseOrg(BaseModel):
    name = models.CharField(max_length=50, verbose_name="organization name")
    desc = models.TextField(verbose_name='description')
    tag = models.CharField(default="famous", max_length=10, verbose_name="organization tag")
    category = models.CharField(default='institution', verbose_name=u"category", max_length=20,
                                choices=(("institution", "institution"), ("person", "person"), ('university', 'university')))
    click_nums = models.IntegerField(default=0, verbose_name="click numbers")
    fav_nums = models.IntegerField(default=0, verbose_name="fav numbers")
    image = models.ImageField(upload_to="org/%Y/%m", verbose_name=u"logo", max_length=100)
    address = models.CharField(max_length=150, verbose_name="address")
    students = models.IntegerField(default=0, verbose_name="number of students")
    course_nums = models.IntegerField(default=0, verbose_name="course number")
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='city')
    is_auth = models.BooleanField(default=False, verbose_name="authentication")
    is_gold = models.BooleanField(default=False, verbose_name="golden")


    def courses(self):
        # from apps.courses.models import Course
        # courses = Course.objects.filter(course_org=self)
        courses = self.course_set.filter(is_classics=True)[:3]
        return courses



    class Meta:
        verbose_name = "organization"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Teacher(BaseModel):
    org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name="organization")
    name = models.CharField(max_length=50, verbose_name=u"teacher's name")
    work_years = models.IntegerField(default=0, verbose_name='work years')
    work_company = models.CharField(max_length=50, verbose_name="work company")
    work_position = models.CharField(max_length=50, verbose_name="position")
    points = models.CharField(max_length=50, verbose_name="points")
    click_nums = models.IntegerField(default=0, verbose_name="click numbers")
    fav_nums = models.IntegerField(default=0, verbose_name="fav numbers")
    age = models.IntegerField(default=18, verbose_name="age")
    image = models.ImageField(upload_to="teacher/%Y/%m", verbose_name="cover image", max_length=100)

    class Meta:
        verbose_name = 'teacher'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def course_nums(self):
        return self.course_set.all().count()