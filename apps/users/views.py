from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
import redis
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.users.forms import LoginForm, DynamicLoginForm, DynamicLoginPostForm, RegisterGetForm, RegisterPostForm, UploadImageForm, UpdateMobileForm
from apps.users.forms import UserInfoForm
from apps.users.models import UserProfile
#from apps.utils.YunPian import send_single_sms
from apps.utils.random_str import generate_random
#from MxOnline.settings import yp_apikey, REDIS_HOST, REDIS_PORT


class ChangeMobileView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        mobile_form = UpdateMobileForm(request.POST)
        if mobile_form.is_valid():
            mobile = mobile_form.cleaned_data["mobile"]
            #已经存在的记录不能重复注册
            if UserProfile.objects.filter(mobile=mobile):
                return JsonResponse({
                    "status": "fail"
                })
            user = request.user
            user.mobile = mobile
            user.username = mobile
            user.save()
            # logout(request)
            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse(mobile_form.errors)


class UploadImageView(LoginRequiredMixin, View):
    login_url = "/login/"

    # def save_file(self, file):
    #     with open("/Users/yucao/PycharmProjects/MxOnline/media/head_image/uploaded.jpg", "wb") as f:
    #         for chunk in file.chunks():
    #             f.write(chunk)

    def post(self, request, *args, **kwargs):
        #处理用户上传的头像
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse({
                "status": "fail"
            })



class UserInfoView(LoginRequiredMixin, View):
    login_url = "/login/"
    def get(self, request, *args, **kwargs):    #返回页面
        captcha_form = RegisterGetForm()
        return render(request, "usercenter-info.html", {
            "captcha_form": captcha_form,
        })

    def post(self, request, *args, **kwargs):
        user_info_form = UserInfoForm(request.POST, instance=request.user)    #当前的实例，说明是修改的操作
        if user_info_form.is_valid():
            user_info_form.save()
            return JsonResponse({
                "status": "success",
            })
        else:
            return JsonResponse(user_info_form.errors)



class RegisterView(View):
    def get(self, request, *args, **kwargs):    #返回页面
        register_get_form = RegisterGetForm()
        return render(request, "register.html", {
            "register_get_form": register_get_form,
        })

    def post(self, request, *args, **kwargs):    #处理用户传递过来的请求
        register_post_form = RegisterPostForm(request.POST)
        dynamic_login = True
        if register_post_form.is_valid():
            # 注册账号
            mobile = register_post_form.cleaned_data["mobile"]
            password = register_post_form.cleaned_data["password"]
            # 新建一个用户
            user = UserProfile(username=mobile)
            user.set_password(password)  # 生成该密码的秘文
            user.mobile = mobile
            user.save()
            login(request, user)  # 使该用户登陆
            return HttpResponseRedirect(reverse("index"))  # 跳转到首页

        else:
            register_get_form = RegisterGetForm()    #新的验证码
            # register_post_form = RegisterPostForm()    #错误的信息
            return render(request, "register.html", {
                "register_get_form": register_get_form,
                "register_post_form": register_post_form,
            })  # 传递到html文件中


#用户的动态验证码登陆
class DynamicLoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        next = request.GET.get("next", "")
        login_form = DynamicLoginForm()
        return render(request, "login.html", {
            "login_form": login_form,
            "next": next,
        })

    def post(self, request, *args, **kwargs):
        login_form = DynamicLoginPostForm(request.POST)
        dynamic_login = True
        if login_form.is_valid():
            #没有注册账号依然可以登陆
            mobile = login_form.cleaned_data["mobile"]
            code = login_form.cleaned_data["code"]

            existed_users = UserProfile.objects.filter(mobile=mobile)
            if existed_users:
                user = existed_users[0]
            else:
                #新建一个用户
                user = UserProfile(username=mobile)
                password = generate_random((10, 2))    #生成用户首次登陆的随机密码
                user.set_password(password)    #生成该密码的秘文
                user.mobile = mobile
                user.save()
            login(request, user)    #使该用户登陆
            next = request.GET.get("next", "")
            if next:
                return HttpResponseRedirect(next)
            return HttpResponseRedirect(reverse("index"))    #跳转到首页

        else:
            d_form = DynamicLoginForm()
            return render(request, "login.html", {"login_form": login_form,
                                                  "d_form": DynamicLoginForm,
                                                  "dynamic_login": dynamic_login})    #传递到html文件中



class SendSmsView(View):
    def post(self, request, *args, **kwargs):
        # send_sms_form = DynamicLoginForm(request.POST)
        # re_dict = {}
        # if send_sms_form.is_valid():
        #     mobile = send_sms_form.cleaned_data["mobile"]
        #     #随机生成数字验证码
        #     code = generate_random(4, 0)
        #     re_json = send_single_sms(yp_apikey, code, mobile=mobile)
        #     if re_json["code"] == 0:
        #         re_dict["status"] = "success"
        #         r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, charset="utf8", decode_responses=True)
        #         r.set(str(mobile), code)
        #         r.expire(str(mobile), 60 * 5)  设置验证码5分钟过期
        #     else:
        #         re_dict["msg"] = re_json["msg"]
        # else:
        #     for key, value in send_sms_form.errors.items():
        #         re_dict[key] = value[0]
        re_dict = {}
        re_dict["status"] = "success"
        return JsonResponse(re_dict)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))
        next = request.GET.get("next", "")
        login_form = DynamicLoginForm()
        return render(request, "login.html", {
            "login_form": login_form,
            "next": next,
        })

    def post(self, request, *args, **kwargs):
        #表单验证（表单：用户通过前端提交过来的数据）
        # if not user_name:
        #     return render(request, "login.html", {"msg": "user is not exist"})
        # if not password:
        #     return render(request, "login.html", {"msg": "password is wrong"})
        # if len(password) < 3:
        #     return render(request, "login.html", {"msg": "password is wrong"})
        login_form = LoginForm(request.POST)    #1.表单验证；2.对数据加工处理
        user_name = request.POST.get("username", "")
        password = request.POST.get("password", "")

        if login_form.is_valid():
            # 用于通过用户和密码查询用户是否存在
            # user_name = login_form.cleaned_data["username"]
            # password = login_form.cleaned_data["password"]
            user = authenticate(username=user_name, password=password)
            #为什么不采用UserProfile方法
            #1. 通过用户名查询到用户
            #2. 需要先加密再通过加密之后的密码查询
            #user = UserProfile.objects.get(username=user_name, password=password)
            if user is not None:
                #查询到用户
                login(request, user)
                #登陆成功之后应该怎么返回页面
                next = request.GET.get("next", "")
                if next:
                    return HttpResponseRedirect(next)
                return HttpResponseRedirect(reverse("index"))
            else:
                #未查询到用户
                return render(request, "login.html", {"msg":"user is not exist or password is wrong", "login_form": login_form})
        else:
            return render(request, "login.html", {"login_from": login_form})