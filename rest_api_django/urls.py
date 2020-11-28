from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from restApi import views, user_event_views, seed_data, event_views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r"sign_up/", views.SignUp.as_view()),
    url(r"login/", views.Login.as_view()),
    url(r"user_topics/", views.UserTopic.as_view()),
    url(r"topics/", views.TopicOfInterest.as_view()),
    url(r"events", event_views.EventView.as_view()),
    url(r"user/event/", user_event_views.UserEventViews.as_view()),
    url(r"seed_data", seed_data.populateTables),
    url(r"delete_all", seed_data.deleteAllRecordsFromAllTables)
]
