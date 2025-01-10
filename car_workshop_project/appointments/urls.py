from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('', views.home, name='home'),  # Homepage
    path('book/', views.booking_page, name='booking_page'),  # Booking page
    path('success/', views.success_page, name='success_page'),  # Success page
    path('admin-panel/', views.admin_panel, name='admin_panel'),  # Admin panel
    path('admin-logout/', views.admin_logout, name='admin_logout'),  # Admin logout
    path('edit-appointment/<int:appointment_id>/', views.edit_appointment, name='edit_appointment'),  # Edit appointment
    path('view-appointment/', views.view_appointment, name='view_appointment'),
]
