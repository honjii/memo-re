from django.urls import path, include
from rest_framework import routers

from . import views
from .views import FriendListRequestAPIView
from .views import FriendRequestApplyAPIView
from .views import FriendRequestDeleteAPIView

router = routers.DefaultRouter()

app_name = 'apiv1'
urlpatterns = [
    path('', include(router.urls)),
    path('friends/apply/<int:user_from>/',
         views.FriendRequestApplyAPIView.as_view()),
    path('friends/delete/<int:user_to>/',
         views.FriendRequestDeleteAPIView.as_view()),
    path('friends/<int:user_to>/', views.FriendDeleteAPIView.as_view()),
    path('friends/', views.FriendListRequestAPIView.as_view()),
    path('brains/share/<int:note>/<int:user_to>/',
         views.NoteShareUpdateDestroyAPIView.as_view()),
    path('brains/share/',
         views.NoteShareCreateAPIView.as_view()),
    path('brains/<int:id>/',
         views.NoteRetrieveUpdateDestroyAPIView.as_view()),
    path('brains/', views.NoteListCreateAPIView.as_view()),
]
