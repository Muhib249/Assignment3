from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            'client_name', 
            'address', 
            'phone', 
            'car_license_number', 
            'car_engine_number', 
            'appointment_date', 
            'mechanic'
        ]  # Include all required fields
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
        }

class AppointmentEditForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['appointment_date', 'mechanic']  # Restrict editable fields
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
        }

