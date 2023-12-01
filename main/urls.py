from django.urls import path
from . import views
from .apps import MainConfig

app_name = MainConfig.name

urlpatterns = [
   path('', views.MainListView.as_view(), name='home'),
   path('create/channel/', views.СhannelCreateView.as_view(), name='create_channel'),
   path('update/channel/<int:pk>', views.СhannelUpdateView.as_view(), name='update_channel'),
   path("channel/<str:channel_name>/", views.СhannelDetailView.as_view(), name='detail'),
]
