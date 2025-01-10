from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Mechanic, Appointment
from .forms import AppointmentForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from .models import Appointment
from django.shortcuts import get_object_or_404, render, redirect
from .forms import AppointmentEditForm


def home(request):
    # Homepage with only two options: Admin Login and Book Appointment button
    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_superuser:  # Check if the user is a superuser
                login(request, user)
                return redirect('/admin')  # Redirect superuser to Django admin
            elif user.groups.filter(name='Workshop Admin').exists():  # Check if the user is in Workshop Admin group
                login(request, user)
                return redirect('appointments:admin_panel')  # Redirect Workshop Admin to admin panel
            else:
                error_message = "You don't have the required permissions to access the admin panel."
        else:
            error_message = "Invalid admin credentials."

    return render(request, 'appointments/home.html', {'error_message': error_message})

def admin_logout(request):
    logout(request)  # Logs out the current user
    messages.success(request, "You have been logged out successfully.")
    return redirect('appointments:home')  # Redirect to the homepage

@login_required
def admin_panel(request):
    if not request.user.is_staff:
        # Redirect non-admin users back to the home page with an error
        messages.error(request, "You do not have permission to access this page.")
        return redirect('appointments:home')

    # Fetch all appointments to display in the admin panel
    appointments = Appointment.objects.select_related('mechanic').order_by('-appointment_date')
    return render(request, 'appointments/admin_panel.html', {
        'appointments': appointments,
        'total_appointments': appointments.count()
    })

# def success_page(request):
#     return render(request, 'appointments/success.html')

def booking_page(request):
    # Booking form view
    mechanics = Mechanic.objects.all()
    form = AppointmentForm()

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            mechanic = form.cleaned_data['mechanic']
            date = form.cleaned_data['appointment_date']
            
            if mechanic.get_available_slots(date) > 0:
                form.save()
                messages.success(request, 'Appointment booked successfully!')
                return redirect('appointments:success_page')
            else:
                messages.error(request, 'Selected mechanic is fully booked for this date.')

    return render(request, 'appointments/booking_page.html', {
        'form': form,
        'mechanics': mechanics
    })
def view_appointment(request):
    appointment = None
    phone_number = None
    error_message = None

    if request.method == 'POST':
        phone_number = request.POST.get('phone')
        try:
            appointment = Appointment.objects.get(phone=phone_number)
        except Appointment.DoesNotExist:
            error_message = "No appointment found for this phone number."

    return render(request, 'appointments/view_appointment.html', {
        'appointment': appointment,
        'phone_number': phone_number,
        'error_message': error_message,
    })    

def success_page(request):
    # Appointment success confirmation page
    return render(request, 'appointments/success.html')
    # Check if the user belongs to the Workshop Admin group
# Check if the user is in the Workshop Admin group
# Check if the user is in the Workshop Admin group
def is_workshop_admin(user):
    return user.groups.filter(name='Workshop Admin').exists()

@login_required
@user_passes_test(is_workshop_admin)  # Restrict to Workshop Admins only
def edit_appointment(request, appointment_id):
    # Get the specific appointment
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Ensure user has the correct permissions
    if not (request.user.has_perm('appointments.change_appointment') or
            request.user.has_perm('appointments.change_mechanic')):
        messages.error(request, "You do not have permission to edit this appointment.")
        return redirect('appointments:admin_panel')

    # Handle form submission
    if request.method == 'POST':
        form = AppointmentEditForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, "Appointment updated successfully!")
            return redirect('appointments:admin_panel')
    else:
        form = AppointmentEditForm(instance=appointment)

    return render(request, 'appointments/edit_appointment.html', {
        'form': form,
        'appointment': appointment
    })
