from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Main URLs
    path('', views.kirana, name='kirana'),
    path('add/', views.add_data, name='add_data'),
    path('all/', views.all, name='all'),
    path('all/<slug:slug>/', views.detail, name='detail'),
    path('delete/<slug:slug>/', views.delete_receipt, name='delete_receipt'),
    path('contact/', views.contact, name='contact'),
]

