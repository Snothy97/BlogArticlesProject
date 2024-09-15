$(document).ready(function() {
    $('#submitUserBtn').click(function(event) {
        event.preventDefault(); 

        var userRole = $('#user_role').val();
        var firstName = $('#first_name').val();
        var lastName = $('#last_name').val();
        var idNumber = $('#id_number').val();
        var phoneNumber = $('#phone_number').val();
        var email = $('#email').val();

        if (!userRole || !firstName || !lastName || !idNumber || !phoneNumber || !email) {
            Swal.fire({
                title: 'Error!',
                text: 'Please fill in all the fields.',
                icon: 'error',
                confirmButtonText: 'OK'
            });
            return;
        }

        var data = {
            user_type_id: userRole,
            first_name: firstName,
            last_name: lastName,
            id_number: idNumber,
            phone_number: phoneNumber,
            email: email,
            csrfmiddlewaretoken: CSRF_TOKEN 
        };

        $.ajax({
            url: CREATE_USER_URL,
            method: 'POST',
            data: data,
            success: function(response) {
                Swal.fire({
                    title: 'Success!',
                    text: response.message,
                    icon: 'success',
                    confirmButtonText: 'OK'
                }).then(() => {
                   
                    location.reload(); 
                });
            },
            error: function(xhr, status, error) {
                var err = JSON.parse(xhr.responseText);
                Swal.fire({
                    title: 'Error!',
                    text: err.message || 'Something went wrong. Please try again.',
                    icon: 'error',
                    confirmButtonText: 'OK'
                });
            }
        });
    });
   

    $('form[id^="update_user_form_"]').on('submit', function(event) {
        event.preventDefault();

        var form_id = $(this).attr('id');
        var user_id = form_id.split('_')[3];
        var data = {
            first_name: $('#first_name_' + user_id).val(),
            last_name: $('#last_name_' + user_id).val(),
            email: $('#email_' + user_id).val(),
            phone_number: $('#phone_number_' + user_id).val(),
        };
        
        $.ajax({
            url: `/system_management/update_user/${user_id}/`,
            method: 'POST',
            data: JSON.stringify(data),
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': CSRF_TOKEN
            },
            success: function(response) {
                Swal.fire({
                    title: 'Success!',
                    text: response.message,
                    icon: 'success',
                    confirmButtonText: 'OK'
                }).then(() => {
                    location.reload();
                });
            },
            error: function(xhr) {
                Swal.fire({
                    title: 'Error!',
                    text: xhr.responseJSON.error || 'Something went wrong!',
                    icon: 'error',
                    confirmButtonText: 'OK'
                });
            }
        });
    });

    $(document).on('click', '.deactivate_user, .activate_user', function() {
        var user_id = $(this).data('id');
        
        $.ajax({
            url: `/system_management/change_user_status/${user_id}/`,
            headers: {
                'X-CSRFToken': CSRF_TOKEN 
            },
            success: function(response) {
                Swal.fire({
                    title: 'Success!',
                    text: `User has been ${response.status}.`,
                    icon: 'success',
                    confirmButtonText: 'OK'
                }).then(() => {
                    location.reload();
                });
            },
            error: function(xhr) {
                Swal.fire({
                    title: 'Error!',
                    text: xhr.responseJSON.error || 'Something went wrong!',
                    icon: 'error',
                    confirmButtonText: 'OK'
                });
            }
        });
    });
    
    
});
