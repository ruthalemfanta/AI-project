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

document.addEventListener('DOMContentLoaded', function() {
    const infoIconContainers = document.querySelectorAll('.info-icon-container');

    infoIconContainers.forEach(container => {
        container.addEventListener('mouseover', function() {
            const tooltip = container.querySelector('.tooltip');
            const rect = tooltip.getBoundingClientRect();
            const viewportWidth = window.innerWidth;

            container.classList.remove('tooltip-right');

            if (rect.right > viewportWidth) {
                container.classList.add('tooltip-right');
            }
        });
    });
});
