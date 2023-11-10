from django.urls import path
from . import views
from .apps import MainConfig

app_name = MainConfig.name

urlpatterns = [
   path('', views.MainListView.as_view()),
   path('create/channel/', views.СhannelCreateView.as_view()),
   path('update/channel/<int:pk>', views.СhannelUpdateView.as_view()),
   path("channel/<str:channel_name>/", views.СhannelDetailView.as_view(), name='detail'),
   path("create/subscriptions/", views.SubscriptionsCreateView.as_view(), name='create_sub'),
   path("update/subscriptions/<int:pk>", views.SubscriptionsUpdateView.as_view(), name='update_sub'),
   path("delete/subscriptions/<int:pk>", views.SubscriptionsDeleteView.as_view(), name='delete_sub'),
   path('create/post/', views.PostCreateView.as_view(), name='create_post'),
   path("update/post/<int:pk>", views.PostUpdateView.as_view(), name='update_post'),
   path("delete/post/<int:pk>", views.PostDeleteView.as_view(), name='delete_post'),
   path('create/comments/<int:post_id>/', views.СommentsCreateView.as_view(), name='create_comm'),
   path("delete/comments/<int:pk>", views.СommentsDeleteView.as_view(), name='delete_comm'),
   path("update/comments/<int:pk>", views.СommentsUpdateView.as_view(), name='update_comm'),
   path('update-likes/<int:post_id>/', views.UpdateLikesView.as_view(), name='update_likes'),
]