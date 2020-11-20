from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from restApi import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r"sign_up/", views.SignUp.as_view()),
    url(r"login/", views.Login.as_view()),
    url(r"user_topics/", views.UserTopic.as_view()),
    url(r"topics/", views.TopicOfInterest.as_view())
]
