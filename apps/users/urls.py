from django.conf.urls import url
from django.urls import path

from apps.users.views import UserInfoView, UploadImageView, ChangeMobileView

urlpatterns = [
    url(r'^info/$', UserInfoView.as_view(), name='info'),
    url(r'^image/upload/$', UploadImageView.as_view(), name='image'),
    url(r'^image/mobile/$', ChangeMobileView.as_view(), name='update_mobile'),
]
