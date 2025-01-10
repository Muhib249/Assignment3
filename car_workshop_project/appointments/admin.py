from django.contrib import admin
from .models import Mechanic, Appointment

@admin.register(Mechanic)
class MechanicAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'phone', 'car_license_number', 'car_engine_number', 'appointment_date', 'mechanic')
    list_filter = ('appointment_date', 'mechanic')
