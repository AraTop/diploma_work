from django.urls import path
from . import views
from .apps import SubscriptionConfig

app_name = SubscriptionConfig.name


urlpatterns = [
   path("subscriptions/<int:pk>/", views.SubscriptionsDetailView.as_view(), name='detail_sub'),
   path("create/subscriptions/", views.SubscriptionsCreateView.as_view(), name='create_sub'),
   path("update/subscriptions/<int:pk>", views.SubscriptionsUpdateView.as_view(), name='update_sub'),
   path("delete/subscriptions/<int:pk>", views.SubscriptionsDeleteView.as_view(), name='delete_sub'),
   path('subscriptions/', views.SubscriptionsListView.as_view(), name='list_sub'),
]
