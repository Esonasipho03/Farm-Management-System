from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
     path('', views.landing_page, name='landing_page'),
    path('signup/', views.signup, name='signup'),
     path('login/', views.login_view, name='login'),
    path('homee/', views.management_home, name='management_home'),
    
     path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    path('account/', views.account_view, name='account'),
    
    path('crops/', views.crop_list, name='crop_list'),
    path('crops/<int:pk>/', views.crop_detail, name='crop_detail'),
    path('crops/edit/<int:pk>/', views.crop_edit, name='crop_edit'),
    path('crops/add/', views.crop_edit, name='crop_add'),
    path('crops/delete/<int:pk>/', views.crop_delete, name='crop_delete'),
    
    path('live/', views.live_list, name='live_list'),
    path('live/<int:pk>/', views.live_detail, name='live_detail'),
    path('live/edit/<int:pk>/', views.live_edit, name='live_edit'),
    path('live/add/', views.live_edit, name='live_add'),
    path('live/delete/<int:pk>/', views.live_delete, name='live_delete'),
    path('search/', views.search_view, name='search'),
    
    
    path('equipment/', views.equipment_schedule, name='schedule'),
    path('equipment/edit/<int:pk>/', views.edit_equipment, name='edit_equipment'),
    
    path('livestock-inventory/', views.livestock_inventory_report, name='livestock_inventory_report'),
    path('crop_inventory/', views.crop_inventory_report, name='crop_inventory_report'),
    
     path('password_reset/', views.password_reset_request, name='password_reset_request'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
]
