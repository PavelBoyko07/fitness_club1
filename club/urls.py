from django.urls import path

from . import views
from .views import send_sms_view

urlpatterns = [
    path('', views.index, name='home'),
    path('memberships/', views.membership_list, name='membership_list'),
    path('memberships/<slug:slug>/', views.membership_detail, name='membership_detail'),
    path('directions/<slug:slug>/', views.direction_detail, name='direction_detail'),
    path('training-types/', views.training_type_list, name='training_type_list'),
    path('trainers/', views.trainer_list, name='trainer_list'),
    path('trainers/<int:pk>/', views.trainer_detail, name='trainer_detail'),
    path('applications/', views.application_list, name='application_list'),
    path('applications/<int:pk>/', views.application_detail, name='application_detail'),
    path('applications/create/<int:membership_id>/', views.create_application, name='create_application'),
    path('stocks/', views.stock_list, name='stock_list'),
    path('reviews/', views.review_list, name='review_list'),
    path('visits/', views.visit_list, name='visit_list'),
    path('schedule/', views.schedule_type_list, name='schedule_type_list'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('register/', views.register, name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('send-sms/', send_sms_view, name='send_sms'),
]
