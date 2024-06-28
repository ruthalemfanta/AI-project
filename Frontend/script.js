document.getElementById('summarizeForm').addEventListener('submit', function(event) {
    event.preventDefault();
    
    let formData = new FormData(this);
    fetch('/summarize', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('output').value = data.summary;
    })
    .catch(error => console.error('Error:', error));
});

document.getElementById('deleteImage').addEventListener('click', function() {
    document.getElementById('input').value = '';
});