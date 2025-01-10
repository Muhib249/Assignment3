document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const phoneInput = document.querySelector('input[name="phone"]');
    const engineNumberInput = document.querySelector('input[name="car_engine_number"]');
    const appointmentDateInput = document.querySelector('input[name="appointment_date"]');
    const mechanicSelect = document.querySelector('select[name="mechanic"]');

    form.addEventListener('submit', function(event) {
        let valid = true;

        // Validate phone number
        if (!/^\d{10}$/.test(phoneInput.value)) {
            alert('Please enter a valid 10-digit phone number.');
            valid = false;
        }

        // Validate engine number
        if (!/^\d+$/.test(engineNumberInput.value)) {
            alert('Please enter a valid engine number.');
            valid = false;
        }

        // Validate appointment date
        if (!appointmentDateInput.value) {
            alert('Please select an appointment date.');
            valid = false;
        }

        // Validate mechanic selection
        if (!mechanicSelect.value) {
            alert('Please select a mechanic.');
            valid = false;
        }

        if (!valid) {
            event.preventDefault();
        }
    });
});
