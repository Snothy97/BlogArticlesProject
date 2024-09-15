$(document).ready(function() {

    $('#createArticleForm').on('submit', function(event) {
        event.preventDefault(); 


        var formData = new FormData($('#createArticleForm')[0]);

        formData.append('csrfmiddlewaretoken', CSRF_TOKEN);

        $.ajax({
            url: CREATE_ARTICLE_URL, 
            type: 'POST',
            data: formData,
            contentType: false,  // Important for file upload
            processData: false,
            success: function(response) {
                console.log("Success response:", response.status);
                if (response.status === 'success') {
                    Swal.fire({
                        title: 'Success!',
                        text: response.message,
                        icon: 'success',
                        confirmButtonText: 'OK'
                    }).then(() => {
                        location.reload(); // Reload page on success
                    });
                }
            },
            error: function(xhr) {
                console.log("Error response:", xhr);
                var errors = JSON.parse(xhr.responseText);
                Swal.fire({
                    title: 'Error!',
                    text: errors.error,
                    icon: 'error',
                    confirmButtonText: 'OK'
                });
            }
        });
    });
    
    // Update Article
    $('form[id^="editArticleForm_"]').on("submit", function (event) {
        event.preventDefault();
        var formId = $(this).attr('id');
        var articleId = formId.split('_')[1]; 

        var formData = $(this).serialize();

        $.ajax({
            url: `/BLOG/update_article/${articleId}/`,
            type: 'POST',
            data: formData,
            headers: {
                'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val() 
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
                console.log("Error response:", xhr);
                var errors = JSON.parse(xhr.responseText);
                Swal.fire({
                    title: 'Error!',
                    text: errors.error,
                    icon: 'error',
                    confirmButtonText: 'OK'
                });
            }
        });
    });

    $('.delete-article').on('click',function(event) {
        event.preventDefault();
        var article_id = $(this).data('id');
        var csrfToken = CSRF_TOKEN

        if (confirm('Are you sure you want to delete this article?')) {
            $.ajax({
                url: `/BLOG/delete_article/${article_id}/`,
                type: 'DELETE',
                headers: {
                    'X-CSRFToken': csrfToken
                },
                success: function(response) {
                    console.log("Success response:", response.status);
                    if (response.status === 'success') {
                        Swal.fire({
                            title: 'Success!',
                            text: response.message,
                            icon: 'success',
                            confirmButtonText: 'OK'
                        }).then(() => {
                            location.reload(); 
                        });
                    }
                },
                error: function(xhr) {
                    console.log("Error response:", xhr);
                    var errors = JSON.parse(xhr.responseText);
                    Swal.fire({
                        title: 'Error!',
                        text: errors.error,
                        icon: 'error',
                        confirmButtonText: 'OK'
                    });
                }
            });
        }
    });
});
