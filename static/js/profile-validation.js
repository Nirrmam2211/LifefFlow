document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    if (!form) return;

    form.addEventListener('submit', function(event) {
        let isValid = true;
        const errorMessages = [];

        // Validate name
        const name = document.getElementById('name').value.trim();
        if (name.length < 2 || !/^[A-Za-z .]+$/.test(name)) {
            isValid = false;
            errorMessages.push('Please enter a valid name (only letters, spaces, and dots, minimum 2 characters)');
        }

        // Validate age
        const age = parseInt(document.getElementById('age').value);
        if (isNaN(age) || age < 18 || age > 65) {
            isValid = false;
            errorMessages.push('Age must be between 18 and 65');
        }

        // Validate contact
        const contact = document.getElementById('contact').value.trim();
        if (!/^[0-9]{10,}$/.test(contact)) {
            isValid = false;
            errorMessages.push('Please enter a valid contact number (minimum 10 digits)');
        }

        // Validate email
        const email = document.getElementById('email').value.trim();
        if (!/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/.test(email)) {
            isValid = false;
            errorMessages.push('Please enter a valid email address');
        }

        // Validate address
        const address = document.getElementById('address').value.trim();
        if (address.length < 10) {
            isValid = false;
            errorMessages.push('Please enter a complete address (minimum 10 characters)');
        }

        if (!isValid) {
            event.preventDefault();
            // Display error messages
            const errorContainer = document.getElementById('error-container');
            if (errorContainer) {
                errorContainer.innerHTML = errorMessages.map(msg => 
                    `<div class="p-4 mb-2 bg-red-100 text-red-800 rounded-md">${msg}</div>`
                ).join('');
                errorContainer.scrollIntoView({ behavior: 'smooth' });
            }
        }
    });
});