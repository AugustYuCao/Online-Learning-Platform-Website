import re
from django import forms
from apps.operations.models import UserFavorite, CourseComments

# class AddAskForm(forms.Form):
#     name = forms.CharField(required=True, min_length=2, max_length=20)
#     mobile = forms.CharField(required=True, min_length=11, max_length=9)
#     course_name = forms.CharField(required=True, min_length=2, max_length=20)


class UserFavForm(forms.ModelForm):
    class Meta:
        model = UserFavorite
        fields = ["fav_id", "fav_type"]    #指出我们需要的，生成此form的字段有哪些


class CommentsForm(forms.ModelForm):
    class Meta:
        model = CourseComments
        fields = ["course", "comments"]    #指出我们需要的，生成此form的字段有哪些