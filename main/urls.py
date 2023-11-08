from django.urls import path
from . import views
from .apps import MainConfig

app_name = MainConfig.name

urlpatterns = [
   path('', views.MainListView.as_view()),
   path('create/channel/', views.СhannelCreateView.as_view()),
   path('update/channel/', views.СhannelUpdateView.as_view()),
   path("channel/<str:channel_name>/", views.СhannelDetailView.as_view(), name='detail'),
   path("create/subscriptions/", views.SubscriptionsCreateView.as_view(), name='create_sub'),
   path("update/subscriptions/<int:pk>", views.SubscriptionsUpdateView.as_view(), name='update_sub'),
]