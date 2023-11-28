from django.urls import path
from . import views
from .apps import PaymentConfig

app_name = PaymentConfig.name

urlpatterns = [
   path('create_payment/<int:pk>/', views.PaymentCreateView.as_view(), name='create_payment'),
   path('retrieve_payment/<str:payment_intent_id>/', views.PaymentRetrieveView.as_view(), name='retrieve')
]
