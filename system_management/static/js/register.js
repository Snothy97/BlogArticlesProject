$(document).ready(function() {
    $('#register_form').on('submit', function(event) {
        // Prevent the form from submitting initially
        event.preventDefault();

        // Clear previous error messages
        $('.error').remove();

        // Retrieve form values
        var first_name = $('#first_name').val();
        var last_name = $('#last_name').val();
        var email = $('#email').val();
        var password = $('#password').val();
        var confirm_password = $('#confirm_password').val();

        // Validation flag
        var isValid = true;

        // Validate first name
        if (first_name === '') {
            $('#first_name').after('<span class="error text-danger">First name is required</span>');
            isValid = false;
        }

        // Validate last name
        if (last_name === '') {
            $('#last_name').after('<span class="error text-danger">Last name is required</span>');
            isValid = false;
        }

        // Validate email
        var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            $('#email').after('<span class="error text-danger">Please enter a valid email address</span>');
            isValid = false;
        }

        // Validate password
        if (password.length < 6) {
            $('#password').after('<span class="error text-danger">Password must be at least 6 characters long</span>');
            isValid = false;
        }

        // Validate confirm password
        if (password !== confirm_password) {
            $('#confirm_password').after('<span class="error text-danger">Passwords do not match</span>');
            isValid = false;
        }

        if (isValid) {
            var data = {
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "password": password,
                "confirm_password": confirm_password
            };

            $.ajax({
                url: REGISTER_URL,
                type: 'POST',
                headers: {
                    'X-CSRFToken': CSRF_TOKEN
                },
                data: data,
                success: function(response) {
                    Swal.fire({
                        title: 'Success!',
                        text: response.success,
                        icon: 'success',
                        confirmButtonText: 'OK'
                    }).then(() => {
                        window.location.href = LOGIN_URL;
                    });
                },
                error: function(xhr) {
                    var errorMessage = xhr.responseJSON ? xhr.responseJSON.error : 'An error occurred';
                    Swal.fire({
                        title: 'Error!',
                        text: errorMessage,
                        icon: 'error',
                        confirmButtonText: 'OK'
                    });
                }
            });
        }
    });
});
