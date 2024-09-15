function togglePasswordVisibility() {
  var passwordInput = document.getElementById("password");
  var icon = document.getElementById("toggle-password-icon");

  if (passwordInput.type === "password") {
      passwordInput.type = "text";
      icon.classList.remove("fa-eye");
      icon.classList.add("fa-eye-slash");
  } else {
      passwordInput.type = "password";
      icon.classList.remove("fa-eye-slash");
      icon.classList.add("fa-eye");
  }
}
$('#toggle_login_password').on('click', function () {
  if ($('#password').attr('type') === 'password') {
      $('#password').attr('type', 'text');
      $(this).removeClass('fa-eye').addClass('fa-eye-slash');
  } else {
      $('#password').attr('type', 'password');
      $(this).removeClass('fa-eye-slash').addClass('fa-eye');
  }
  });

  $(document).ready(function() {
    $('#login_btn').on('click', function(e) {
        e.preventDefault();
     
        var email = $('#email').val();
        var password = $('#password').val();

        // Check if email and password are provided
        if (!email || !password) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Please fill in both email and password fields',
            });
            return;
        }

        // Send the login request to the backend
        $.ajax({
            url: LOGIN_URL, 
            type: 'POST',
            headers: {
                'X-CSRFToken': CSRF_TOKEN
            },
            data: {
                'email': email,
                'password': password
            },
            success: function(response) {
                // If login is successful, redirect to the home page
                if (response.success) {
                    Swal.fire({
                        icon: 'success',
                        title: 'Success',
                        text: 'Login successful! Redirecting...',
                    }).then(() => {
                        window.location.href = BLOG_URL;  // Redirect to home
                    });
                } else {
                    // If login fails, show error message
                    Swal.fire({
                        icon: 'error',
                        title: 'Login Failed',
                        text: response.message,
                    });
                }
            },
            error: function(xhr, status, error) {
                Swal.fire({
                    icon: 'error',
                    title: 'Error',
                    text: 'An error occurred while trying to log in. Please try again.',
                });
            }
        });
    });
});
