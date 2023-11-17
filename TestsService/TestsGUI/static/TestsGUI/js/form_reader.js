function submitForm() {
    const form = document.getElementById('answerForm');
    const checkboxes = form.querySelectorAll('input[type="checkbox"]:checked');

    const selectedAnswers = Array.from(checkboxes).map(checkbox => checkbox.value);

    // Construct the URL for the next page with selected answers
    const nextPageUrl = `/tests/${nextQuestion}/?selected=${selectedAnswers.join(',')}`;

    // Redirect to the next page
    window.location.href = nextPageUrl;
}