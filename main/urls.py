from django.urls import path
from . import views

urlpatterns = [
   path('', views.MainListView.as_view()),
   path('create/channel/', views.СhannelCreateView.as_view()),
   path("channel/<str:channel_name>/", views.СhannelDetailView.as_view(), name='detail'),
]