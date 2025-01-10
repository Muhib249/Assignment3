from django.db import models
from django.core.exceptions import ValidationError

class Mechanic(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    
    def get_available_slots(self, date):
        appointments = self.appointments.filter(appointment_date=date)
        return 4 - appointments.count()

    def __str__(self):
        return self.name

class Appointment(models.Model):
    client_name = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    car_license_number = models.CharField(max_length=20)
    car_engine_number = models.CharField(max_length=20)
    appointment_date = models.DateField()
    mechanic = models.ForeignKey(Mechanic, on_delete=models.CASCADE, related_name='appointments')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['car_engine_number', 'appointment_date']