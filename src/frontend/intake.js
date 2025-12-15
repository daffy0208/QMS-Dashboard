// QMS Dashboard - Intake Form JavaScript
// Handles form validation and submission

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('intakeForm');
    const errorMessage = document.getElementById('errorMessage');
    const submitBtn = form.querySelector('.submit-btn');

    // Form submission handler
    form.addEventListener('submit', async function(e) {
        e.preventDefault();

        // Clear previous errors
        hideError();

        // Validate all questions are answered
        if (!validateForm()) {
            showError('Please answer all 7 questions before submitting.');
            return;
        }

        // Collect form data
        const intakeData = collectFormData();

        // Disable submit button during submission
        submitBtn.disabled = true;
        submitBtn.textContent = 'Processing...';

        try {
            // Submit to backend API
            const response = await submitIntake(intakeData);

            // Handle successful submission
            handleSuccess(response);
        } catch (error) {
            // Handle errors
            showError('Error submitting intake: ' + error.message);
            submitBtn.disabled = false;
            submitBtn.textContent = 'Submit Intake';
        }
    });

    // Validate that all questions have been answered
    function validateForm() {
        const questions = [
            'q1_users',
            'q2_influence',
            'q3_worst_failure',
            'q4_reversibility',
            'q5_domain',
            'q6_scale',
            'q7_regulated'
        ];

        for (const question of questions) {
            const answered = form.querySelector(`input[name="${question}"]:checked`);
            if (!answered) {
                return false;
            }
        }

        return true;
    }

    // Collect all form data into structured object
    function collectFormData() {
        const formData = new FormData(form);
        const projectName = prompt('What is the name of this project?', 'QMS Dashboard');

        return {
            project_name: projectName || 'Unnamed Project',
            timestamp: new Date().toISOString(),
            answers: {
                q1_users: formData.get('q1_users'),
                q2_influence: formData.get('q2_influence'),
                q3_worst_failure: formData.get('q3_worst_failure'),
                q4_reversibility: formData.get('q4_reversibility'),
                q5_domain: formData.get('q5_domain'),
                q6_scale: formData.get('q6_scale'),
                q7_regulated: formData.get('q7_regulated')
            }
        };
    }

    // Submit intake data to backend API
    async function submitIntake(data) {
        const response = await fetch('/api/intake', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to submit intake');
        }

        return await response.json();
    }

    // Handle successful submission
    function handleSuccess(response) {
        // Store response for results page
        sessionStorage.setItem('intakeResponse', JSON.stringify(response));

        // Redirect to results page (to be created)
        window.location.href = 'results.html';
    }

    // Show error message
    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.style.display = 'block';
        errorMessage.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    // Hide error message
    function hideError() {
        errorMessage.style.display = 'none';
        errorMessage.textContent = '';
    }

    // Add visual feedback when options are selected
    const radioInputs = form.querySelectorAll('input[type="radio"]');
    radioInputs.forEach(radio => {
        radio.addEventListener('change', function() {
            // Remove selected styling from all options in this question
            const questionBlock = this.closest('.question-block');
            const options = questionBlock.querySelectorAll('.option');
            options.forEach(opt => {
                opt.style.borderColor = '#e0e0e0';
                opt.style.backgroundColor = 'white';
            });

            // Add selected styling to chosen option
            const selectedOption = this.closest('.option');
            selectedOption.style.borderColor = '#3498db';
            selectedOption.style.backgroundColor = '#f0f8ff';
        });
    });
});
