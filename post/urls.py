from django.urls import path
from . import views
from .apps import PostConfig

app_name = PostConfig.name

urlpatterns = [
   path('create/post/', views.PostCreateView.as_view(), name='create_post'),
   path("update/post/<int:pk>", views.PostUpdateView.as_view(), name='update_post'),
   path("delete/post/<int:pk>", views.PostDeleteView.as_view(), name='delete_post'),
   path('create/comments/<int:post_id>/', views.СommentsCreateView.as_view(), name='create_comm'),
   path("delete/comments/<int:pk>", views.СommentsDeleteView.as_view(), name='delete_comm'),
   path("update/comments/<int:pk>", views.СommentsUpdateView.as_view(), name='update_comm'),
   path('update-likes/<int:post_id>/', views.UpdateLikesView.as_view(), name='update_likes'),
]
