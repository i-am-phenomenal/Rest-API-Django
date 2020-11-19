from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from restApi import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r"sign_up/", views.SignUp.as_view()),
    url(r"login/", views.Login.as_view()),
    url(r"user/topics/add", views.UserTopic.as_view()),
    url(r"topics/add", views.TopicOfInterest.as_view())
]
