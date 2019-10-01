from django import forms
from captcha.fields import CaptchaField
import redis

from MxOnline.settings import REDIS_HOST, REDIS_PORT
from apps.users.models import UserProfile

class UpdateMobileForm(forms.Form):
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    code = forms.CharField(required=True, min_length=4, max_length=4)

    def clean_code(self):
        mobile = self.data.get("mobile")  # 用户填写的mobile,经调用clean之后
        code = self.data.get("code")  # 用户填写的code,经调用clean之后

        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf8", decode_responses=True)  # 与redis库建立连接
        redis_code = r.get(str(mobile))  # 从redis库中提取API发送的redis_code
        if code != redis_code:  # 如果从redis库中找到的redis_code与用户输入的code不相等
            raise forms.ValidationError("the code is wrong")  # 抛出异常
        return self.cleaned_data


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["nick_name", "gender", "birthday", "address"]



class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["image"]


class RegisterGetForm(forms.Form):    #用于注册的手机验证码
    captcha = CaptchaField()


class RegisterPostForm(forms.Form):
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    code = forms.CharField(required=True, min_length=4, max_length=4)
    password = forms.CharField(required=True, min_length=3)

    def clean_mobile(self):
        mobile = self.data.get("mobile")

        #验证手机号码是否已经注册
        users = UserProfile.objects.filter(mobile=mobile)
        if users:
            raise forms.ValidationError("the telephone number is already registered.")
        return mobile

    def clean_code(self):
        mobile = self.data.get("mobile")  # 用户填写的mobile,经调用clean之后
        code = self.data.get("code")  # 用户填写的code,经调用clean之后

        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf8", decode_responses=True)  # 与redis库建立连接
        redis_code = r.get(str(mobile))  # 从redis库中提取API发送的redis_code
        if code != redis_code:  # 如果从redis库中找到的redis_code与用户输入的code不相等
            raise forms.ValidationError("the code is wrong")  # 抛出异常

        return code


class LoginForm(forms.Form):
    username = forms.CharField(required=True, min_length=2)
    password = forms.CharField(required=True, min_length=3)


class DynamicLoginForm(forms.Form):
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    captcha = CaptchaField()


class DynamicLoginPostForm(forms.Form):
    mobile = forms.CharField(required=True, min_length=11, max_length=11)
    code = forms.CharField(required=True, min_length=4, max_length=4)

    def clean_code(self):
        mobile = self.data.get("mobile")  # 用户填写的mobile,经调用clean之后
        code = self.data.get("code")  # 用户填写的code,经调用clean之后

        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf8", decode_responses=True)  # 与redis库建立连接
        redis_code = r.get(str(mobile))  # 从redis库中提取API发送的redis_code
        if code != redis_code:  # 如果从redis库中找到的redis_code与用户输入的code不相等
            raise forms.ValidationError("the code is wrong")  # 抛出异常
        return self.cleaned_data

    # def clean(self):
    #     mobile = self.cleaned_data["mobile"]    #用户填写的mobile
    #     code = self.cleaned_data["code"]    #用户填写的code
    #
    #     r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf8", decode_responses=True)    #与redis库建立连接
    #     redis_code = r.get(str(mobile))    #从redis库中提取API发送的redis_code
    #     if code != redis_code:    #如果从redis库中找到的redis_code与用户输入的code不相等
    #         raise forms.ValidationError("the code is wrong")    #抛出异常
    #     return self.cleaned_data