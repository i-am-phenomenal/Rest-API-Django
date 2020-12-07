from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from restApi import views, user_event_views, seed_data, event_views, admin_event_view, admin_view, admin_topic_view, admin_topic_event_view
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r"admintopic", admin_topic_view.AdminTopicView, "restApi")
router.register(r"admin_topic_event", admin_topic_event_view.AdminTopicEventView, "restApi")

urlpatterns = [
    path("add_admin/", admin_view.AdminView.as_view()),
    path("api/admin_topic_event/<int:topicEventRelationshipId>/", admin_topic_event_view.GetAdminTopicEventView.as_view()),
    path("api/", include(router.urls)),
    path('admin/event', admin_event_view.AdminEventView.as_view()),
    url(r"sign_up/", views.SignUp.as_view()),
    url(r"login/", views.Login.as_view()),
    url(r"user_topics/", views.UserTopic.as_view()),
    url(r"topics/", views.TopicOfInterest.as_view()),
    url(r"events", event_views.EventView.as_view()),
    url(r"user/event", user_event_views.UserEventViews.as_view()),
    url(r"seed_data", seed_data.populateTables),
    url(r"delete_all", seed_data.deleteAllRecordsFromAllTables)
]
