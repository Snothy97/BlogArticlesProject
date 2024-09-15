document.addEventListener("DOMContentLoaded", function () {
    const idTypeIdRadio = document.getElementById("id_type_id");
    const idTypePassportRadio = document.getElementById("id_type_passport");
    const idNumberContainer = document.getElementById("id_number_container");
    const passportNumberContainer = document.getElementById("passport_number_container");

    // Function to toggle visibility based on the selected radio button
    function toggleIdFields() {
        if (idTypeIdRadio.checked) {
            idNumberContainer.style.display = "block";
            passportNumberContainer.style.display = "none";
        } else if (idTypePassportRadio.checked) {
            passportNumberContainer.style.display = "block";
            idNumberContainer.style.display = "none";
        }
    }

    // Run on page load to show the correct field based on initial checked status
    toggleIdFields();

    // Add event listeners to radio buttons
    idTypeIdRadio.addEventListener("change", toggleIdFields);
    idTypePassportRadio.addEventListener("change", toggleIdFields);


    const profileForm = document.getElementById("updateProfileForm");
    const submitButton = document.getElementById("submitProfileUpdate");

    submitButton.addEventListener("click", function (event) {
        event.preventDefault();  // Prevent default form submission

        const formData = new FormData(profileForm);  // Get form data

        fetch("{% url 'update_profile' %}", {
            method: "POST",
            headers: {
                "X-CSRFToken": "{{ csrf_token }}",  // CSRF Token for security
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            const resultDiv = document.getElementById("updateResult");
            if (data.success) {
                resultDiv.innerHTML = `<div class="alert alert-success">${data.message}</div>`;
            } else {
                resultDiv.innerHTML = `<div class="alert alert-danger">${data.message}</div>`;
            }
        })
        .catch(error => {
            console.error("Error:", error);
        });
    });
});
